from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, date_valid, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # Create and configure the app.
    myapp = Flask(__name__)
    setup_db(myapp)
    CORS(myapp)
    return myapp


app = create_app()


'''
def paginate(page_request, selection, data_type):
    # Helper function used to determine the which actors or movies to display for a given page.
    page = page_request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    if data_type == ACTORS:
        actors = [actor.format() for actor in selection]
        current_items = actors[start:end]
    elif data_type == MOVIES:
        movies = [movie.format() for movie in selection]
        current_items = movies[start:end]

    return current_items
'''


@app.route('/actors')
@requires_auth('get:actors')
def get_all_actors(payload):
    selection = Actor.query.all()
    actors = [actor.format() for actor in selection]
    # Abort if there are no actors in the database.
    if len(actors) == 0:
        abort(404)
    return jsonify({
        'success': True,
        'actors': actors
    })


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):
    try:
        # Get new actor data from request.
        body = request.get_json()
        req_name = body.get('name', None)
        req_birth_date = body.get('birth_date', None)
        req_gender = body.get('gender', None)

        # Validate that all fields are present, if not, abort.
        if (req_name is None) or (req_birth_date is None) or (req_gender is None):
            return abort(422)

        # Validate that the birth date is the proper format, if not, abort.
        if not date_valid(req_birth_date):
            return abort(422)

        # Validate that the gender is the proper format, if not, abort.
        if (req_gender.upper() != 'M') and (req_gender.upper() != 'F') and (req_gender.upper() != 'X'):
            return abort(422)

        # Format and create the actor object.
        actor = Actor(name=req_name, birth_date=req_birth_date, gender=req_gender.upper())

        # Abort if the actor is already present in the database.
        if actor.is_duplicate():
            abort(422)

        # Otherwise, create a row in the database for the actor.
        actor.insert()
        return jsonify({'success': True, "actor": actor.format()})
    except AuthError:
        abort(422)

# TODO: Why getting 422 for a non-existing ids


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def modify_actor(payload, actor_id):
    try:
        # Find the actor with the given id, if they don't exist abort.
        actor = Actor.query.filter(Actor.actor_id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        # Retrieve the updated actor data.
        body = request.get_json()
        req_name = body.get('name', None)
        req_birth_date = body.get('birth_date', None)
        req_gender = body.get('gender', None)

        # Update the actor with the new values.
        if req_name is not None:
            actor.name = req_name
        if req_birth_date is not None:
            if not date_valid(req_birth_date):
                abort(422)
            actor.birth_date = req_birth_date
        if req_gender is not None:
            if (req_gender.upper() != 'M') and (req_gender.upper() != 'F') and (req_gender.upper() != 'X'):
                return abort(422)
            actor.gender = req_gender.upper()
        actor.update()
        return jsonify({"success": True, "actor": actor.format()})
    except AuthError:
        abort(422)

# TODO: Why getting 422 for a non-existing ids


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    try:
        # Find the actor with the given id, if they don't exist abort.
        actor = Actor.query.filter(Actor.actor_id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({"success": True, "delete": actor_id})
    except AuthError:
        abort(422)


@app.route('/movies')
@requires_auth('get:movies')
def get_all_movies(payload):
    selection = Movie.query.all()
    movies = [movie.format() for movie in selection]

    # Abort if there are no movies in the database.
    if len(movies) == 0:
        abort(404)
    return jsonify({
        'success': True,
        'movies': movies
    })


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):
    try:
        # Get new movie data from request.
        body = request.get_json()
        req_title = body.get('title', None)
        req_release_date = body.get('release_date', None)

        # Validate that all fields are present, if not, abort.
        if (req_title is None) or (req_release_date is None):
            return abort(422)

        # Validate that the birth date is the proper format, if not, abort.
        if not date_valid(req_release_date):
            return abort(422)

        # Format and create the actor object.
        movie = Movie(title=req_title, release_date=req_release_date)

        # Abort if the actor is already present in the database.
        if movie.is_duplicate():
            abort(422)

        # Otherwise, create a row in the database for the actor.
        movie.insert()
        return jsonify({'success': True, "movie": movie.format()})
    except AuthError:
        abort(422)

# TODO: Why getting 422 for a non-existing ids


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def modify_movie(payload, movie_id):
    try:
        # Find the movie with the given id, if it doesn't exist abort.
        movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        # Retrieve the updated movie data.
        body = request.get_json()
        req_title = body.get('title', None)
        req_release_date = body.get('release_date', None)

        # Update the movie with the new values.
        if req_title is not None:
            movie.title = req_title
        if req_release_date is not None:
            if not date_valid(req_release_date):
                abort(422)
            movie.release_date = req_release_date
        movie.update()
        return jsonify({"success": True, "movie": movie.format()})
    except AuthError:
        abort(422)

# TODO: Why getting 422 for a non-existing ids


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    try:
        # Find the movie with the given id, if it doesn't exist abort.
        movie = Movie.query.filter(Movie.movie_id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        movie.delete()
        return jsonify({"success": True, "delete": movie_id})
    except AuthError:
        abort(422)


##################################################
# Error Handling
##################################################


'''
Error handling for 422 Unprocessable entity.
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
Error handler for 401 Unauthorized.
'''


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


'''
Error handler for 400 Bad Request.
'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


'''
Error handler for 404 Not Found.
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
Error handler for AuthError.
'''


'''
@app.errorhandler(AuthError)
def handle_invalid_usage(error):
    return jsonify({
        "success": False,
        "error": error.error,
        "message": error.status_code
    }), error.error
'''


# TODO - Need to change this to app.run()?
# if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    app.run()
