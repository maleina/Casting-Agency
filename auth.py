import os
import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

# AuthError Exception
'''
AuthError Exception is a standardized way to communicate auth failure modes.
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
'''
get_token_auth_header() method
    It attempts to get the header from the request.
        It raises an AuthError if no header is present.
    It attempts to split bearer and the token.
        It raises an AuthError if the header is malformed.
    It returns the token part of the header.
'''


def get_token_auth_header():
    # Obtains the Access Token from the Authorization Header.
    # Perform basic validation.
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


'''
check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:actor')
        payload: decoded jwt payload
    It raises an AuthError if permissions are not included in the payload.
    It raises an AuthError if the requested permission string is not in the payload permissions array.
    It returns true otherwise.
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    return True


'''
verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)
    The token should be an Auth0 token with key id (kid).
    It verifies the token using Auth0 /.well-known/jwks.json.
    It decodes the payload from the token.
    It validates the claims.
    It return the decoded payload.
    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    # Retrieve json web key set from Auth0 for verification process.
    myurl = 'https://%s/.well-known/jwks.json' % (AUTH0_DOMAIN)
    jsonurl = urlopen(myurl)
    content = jsonurl.read().decode(jsonurl.headers.get_content_charset())
    jwks = json.loads(content)

    # Obtain the Authorization Header.
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    # Verify that the key identifier (kid) is present.
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    # Unpack the keys from the header.
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # If the keys are present, decode and return the token payload.
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        # Process any errors according to the appropriate type.
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


'''
@requires_auth(permission) decorator method.
    @INPUTS
        permission: string permission (i.e. 'post:actor')
    It uses the get_token_auth_header method to get the token.
    It uses the verify_decode_jwt method to decode the jwt.
    It uses the check_permissions method validate claims and check the requested permission.
    It returns the decorator which passes the decoded payload to the decorated method.
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
            except AuthError:
                abort(401)
            try:
                payload = verify_decode_jwt(token)
            except AuthError:
                abort(401)
            try:
                check_permissions(permission, payload)
            except AuthError:
                abort(401)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
