# Full Stack Capstone Project: Casting Agency

## Introduction

This project was created as part of Udacity's Full Stack Developer Nanodegree program in order to demonstrate mastery of the skills learned during the program. The goal was to complete the backend API for a casting agency web app. The application:

1) Returns a list of available actors and movies to be cast
2) Provides the ability to add, modify or delete both actors and movies.
3) Implements Rules Based Access Control (RBAC):
    - Casting Agents may only view actors and movies.
    - Casting Directors can do all of the above, plus add and delete actors and modify actors and movies.
    - Executive Producers can do all of the above, plus add or delete movies.

The code follows PEP8 style guidelines.

## Getting Started

### Pre-requisites and Local Development

This project requires that you install Python 3 and pip software on your development workstation. If you wish to do further development on the project, it is recommended that you set up a virtual environment. Please see specific, additional requirements in the *requirements.txt* file. 

### Backend

The project has been developed upon the Flask/SQLAlchemy framework. All necessary dependencies are listed in *requirements.txt*. To easily install all required packages, navigate to the main project directory and run the following from the bash command line.

```bash
pip install -r requirements.txt
```

#### Database Setup

The project was developed using a Postgres database, thereby requiring the installation of this system if you do not already have it installed. A version of the underlying database with sample data can be restored by running the following from the command line:

```bash
psql casting < casting.psql
```

#### Starting the server

The server can be started by executing the following commands from the main project directory:

```bash
source setup.sh    # Sets DATABASE_URL environment variable 
export FLASK_APP=app.py
flask run --reload
```

### Tests

To run the tests included in test_app.py run the following from the command line in the main project directory:

```bash
source .env.testing
dropdb casting_test
createdb casting_test
psql casting_test < casting.psql
python test_app.py
```

Please note that 'dropdb casting_test' can be omitted the first time that the test is run.

## API Reference 

### Base URL

The base url of the live version of the api is: https://maleina-casting.herokuapp.com/. Note that you must specify an endpoint (i.e. /movies) and have a valid token with the appropriate permissions to be able to access the data. In the *.env.testing* file, the TEST_TOKEN variable contains a time-limited valid token that may be used to access all endpoints of the api. See below for other tokens. Otherwise, contact the author (see below) for additional assistance.

When running locally, the backend can be accessed at http://127.0.0.1:5000/.

### Authentication

The application uses Auth0 to provide authentication, authorization and RBAC. 

The following roles exist:
- ```Casting Agent``` - may only view actors and movies.
- ```Casting Director``` - can do all of the above, plus add and delete actors and modify actors and movies.
- ```Executive Producer``` - can do all of the above, plus add or delete movies.

As mentioned above, you must have a valid token with the appropriate permissions to be able to access the data. In the *.env.testing* file, the TEST_TOKEN variable contains a time-limited valid token for the Executive Producer role that may be used to access all endpoints of the api. Similarly, the TEST_DIRECTOR and TEST_ASSISTANT variables contain time-limited tokens for the Casting Director and Casting Assistant roles respectively. Otherwise, contact the author (see below) for additional assistance. 

#### Permissions by Role

Casting Agent:
- ```get:actors```
- ```get:movies```

Casting Director:
- ```get:actors```
- ```get:movies```
- ```post:actors```
- ```patch:actors```
- ```patch:movies```
- ```delete:actors```

Executive Producer:
- ```get:actors```
- ```get:movies```
- ```post:actors```
- ```post:movies```
- ```patch:actors```
- ```patch:movies```
- ```delete:actors```
- ```delete:movies```

### Error Handling

Errors are returned as JSON objects. The object below is an example of an error returned if the user tries to update an actor that does not exist:

```
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```

The API will return the following error types:
- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 422: Not Processable

### Resource Endpoint Library

#### GET /actors

Returns a list of actor objects and the success value.

##### Sample Request

```
curl --location --request GET 'localhost:5000/actors' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM1NzIzOWE4ZDIwZThiYTE0ODU4IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MDUwMjQ0NywiZXhwIjoxNTgwNTg4ODQ3LCJhenAiOiJOMG9IMWI3YW9sWHF0U2pnYzJoS3hGRDZldWx2SlZ0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.M9Zlvn9k62DR_MUko4Rm1EwF1Qpdob7_LDnud9IlZtXMAlUe3X5TTsuaL_qV903xbiBE2qebOMsUhVd49JY9luzCBThHe0P-ibfEIAEcWvHpZbXQ5mfLssoCBz0I9w7kOzuopcOY0YzvXDWXiRcWzWma2cqngCBf4zn-m-gdqspmi9greLzHFh-Mz0O1C0k0LdGO6qpED9EWrQqyl7gShV-KFgZXg3UvxCp0pFK2DY8DAHTA6rX48L5iEcrWKYJ3H789z0SGAeAdtzKAtgNFwxH41BTT-I7vCbanVBbx7zjFUEabcIanwo3kKbk4kN3fc_O-bSySTWeu0TlGXpGySw'
```

##### Sample Response

```
{
    "actors": [
        {
            "actor_id": 1,
            "birth_date": "1979-12-12",
            "gender": "M",
            "name": "Joe Bloggs"
        },
        {
            "actor_id": 2,
            "birth_date": "1970-08-24",
            "gender": "X",
            "name": "Tuffy Slimeball"
        },
        {
            "actor_id": 5,
            "birth_date": "1966-08-31",
            "gender": "F",
            "name": "Pamela Anderson"
        }
    ],
    "success": true
}
```

#### GET /movies

Returns a list of movie objects and the success value.

##### Sample Request

```
curl --location --request GET 'localhost:5000/movies' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM1NzIzOWE4ZDIwZThiYTE0ODU4IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MDUwMjQ0NywiZXhwIjoxNTgwNTg4ODQ3LCJhenAiOiJOMG9IMWI3YW9sWHF0U2pnYzJoS3hGRDZldWx2SlZ0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.M9Zlvn9k62DR_MUko4Rm1EwF1Qpdob7_LDnud9IlZtXMAlUe3X5TTsuaL_qV903xbiBE2qebOMsUhVd49JY9luzCBThHe0P-ibfEIAEcWvHpZbXQ5mfLssoCBz0I9w7kOzuopcOY0YzvXDWXiRcWzWma2cqngCBf4zn-m-gdqspmi9greLzHFh-Mz0O1C0k0LdGO6qpED9EWrQqyl7gShV-KFgZXg3UvxCp0pFK2DY8DAHTA6rX48L5iEcrWKYJ3H789z0SGAeAdtzKAtgNFwxH41BTT-I7vCbanVBbx7zjFUEabcIanwo3kKbk4kN3fc_O-bSySTWeu0TlGXpGySw'
```

##### Sample Response

```
{
    "movies": [
        {
            "movie_id": 2,
            "release_date": "2020-05-03",
            "title": "New Bedtime for Bonzo"
        },
        {
            "movie_id": 3,
            "release_date": "2020-06-03",
            "title": "Cats Big Adventure"
        }
    ],
    "success": true
}
```

#### POST /actors - To add a new actor

Creates a new actor with a unique name and a valid birth date and gender. All fields are required. Dates may be entered in the form of 'July 1, 2020' or '2020-07-01' ('YYYY-MM-DD'). Gender must be in the format 'M' or 'm' for male, 'F' or 'f' for female and 'X' or 'x' for other. Returns the newly created actor object and a success value.

##### Sample Request

```
curl --location --request POST 'localhost:5000/actors' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MDUyMzk5NCwiZXhwIjoxNTgwNjEwMzk0LCJhenAiOiJOMG9IMWI3YW9sWHF0U2pnYzJoS3hGRDZldWx2SlZ0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.dkX2juQeJRWoJmSB8Cn6g3Qra2QiFZwe_Aj_W722CeSXTNBHXpwSFtWSvB7n1_wQR7IcoTUHBIa-y2e-_tj8c2diMhYSkCGz9ffHbrqUPy9at7BLsOe9FW5HhsC2Libhm4rRc7GBNf7EQM8cnzZ1MZdgkzzXYjKlJTo7-Guxwz4mLYhOSEOLEGWrcA3gp9opmxVh0OdJzmzk5pHWYnifRRABXgh0e86JBCtO3eeNyk5-gFYxqzs_bLb3UWNhmugv38fFj8OQzM-XqoGYm5mIL9bIL7Lmkdrp5oekPSZu6K_G4RQytTH7_XAuK_h2vXc2QOfX_Y1U1r5IEeqtmv6NQw' \
--data-raw '{
	"name": "Jane Doe",
	"birth_date": "August 31, 1966",
	"gender": "F"
}'
```

##### Sample Response

```
{
    "actor": {
        "actor_id": 8,
        "birth_date": "1966-08-31",
        "gender": "F",
        "name": "Jane Doe"
    },
    "success": true
}
```

#### POST /movies - To add a new movie

Creates a new movie with a unique title and valid release date. All fields are required. Dates may be entered in the form of 'July 1, 2020' or '2020-07-01' ('YYYY-MM-DD'). Returns the newly created movie object and a success value.

##### Sample Request

```
curl --location --request POST 'localhost:5000/movies' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MDUyMzk5NCwiZXhwIjoxNTgwNjEwMzk0LCJhenAiOiJOMG9IMWI3YW9sWHF0U2pnYzJoS3hGRDZldWx2SlZ0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.dkX2juQeJRWoJmSB8Cn6g3Qra2QiFZwe_Aj_W722CeSXTNBHXpwSFtWSvB7n1_wQR7IcoTUHBIa-y2e-_tj8c2diMhYSkCGz9ffHbrqUPy9at7BLsOe9FW5HhsC2Libhm4rRc7GBNf7EQM8cnzZ1MZdgkzzXYjKlJTo7-Guxwz4mLYhOSEOLEGWrcA3gp9opmxVh0OdJzmzk5pHWYnifRRABXgh0e86JBCtO3eeNyk5-gFYxqzs_bLb3UWNhmugv38fFj8OQzM-XqoGYm5mIL9bIL7Lmkdrp5oekPSZu6K_G4RQytTH7_XAuK_h2vXc2QOfX_Y1U1r5IEeqtmv6NQw' \
--data-raw '{
	"title": "Violent Movie",
	"release_date": "July 4, 2020"
}'
```

##### Sample Response

```
{
    "movie": {
        "movie_id": 6,
        "release_date": "2020-07-04",
        "title": "Violent Movie"
    },
    "success": true
}
```

#### PATCH /actors/{actor_id} - To update an existing actor

Updates the "name", "birth_date" or "gender" for an existing actor. Requires the actor_id. Not all of the other fields are required, just those that must be updated. Dates may be entered in the form of 'July 1, 2020' or '2020-07-01' ('YYYY-MM-DD'). Gender must be in the format 'M' or 'm' for male, 'F' or 'f' for female and 'X' or 'x' for other. Returns the newly updated actor object and a success value.

##### Sample Request

```
curl --location --request PATCH 'localhost:5000/actors/8' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MDUyMzk5NCwiZXhwIjoxNTgwNjEwMzk0LCJhenAiOiJOMG9IMWI3YW9sWHF0U2pnYzJoS3hGRDZldWx2SlZ0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.dkX2juQeJRWoJmSB8Cn6g3Qra2QiFZwe_Aj_W722CeSXTNBHXpwSFtWSvB7n1_wQR7IcoTUHBIa-y2e-_tj8c2diMhYSkCGz9ffHbrqUPy9at7BLsOe9FW5HhsC2Libhm4rRc7GBNf7EQM8cnzZ1MZdgkzzXYjKlJTo7-Guxwz4mLYhOSEOLEGWrcA3gp9opmxVh0OdJzmzk5pHWYnifRRABXgh0e86JBCtO3eeNyk5-gFYxqzs_bLb3UWNhmugv38fFj8OQzM-XqoGYm5mIL9bIL7Lmkdrp5oekPSZu6K_G4RQytTH7_XAuK_h2vXc2QOfX_Y1U1r5IEeqtmv6NQw' \
--data-raw '{
	"gender": "F",
    "name": "Janet Dole"
}'
```

##### Sample Response

```
{
    "actor": {
        "actor_id": 8,
        "birth_date": "1966-08-31",
        "gender": "F",
        "name": "Janet Dole"
    },
    "success": true
}
```

#### PATCH /movies/{movie_id} - To update an existing movie

Updates the "title" and "release_date" for an existing movie. Requires the movie_id. Not all of the other fields are required, just those that must be updated. Dates may be entered in the form of 'July 1, 2020' or '2020-07-01' ('YYYY-MM-DD'). Returns the newly updated movie object and a success value.

##### Sample Request

```
curl --location --request PATCH 'localhost:5000/movies/6' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MDUyMzk5NCwiZXhwIjoxNTgwNjEwMzk0LCJhenAiOiJOMG9IMWI3YW9sWHF0U2pnYzJoS3hGRDZldWx2SlZ0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.dkX2juQeJRWoJmSB8Cn6g3Qra2QiFZwe_Aj_W722CeSXTNBHXpwSFtWSvB7n1_wQR7IcoTUHBIa-y2e-_tj8c2diMhYSkCGz9ffHbrqUPy9at7BLsOe9FW5HhsC2Libhm4rRc7GBNf7EQM8cnzZ1MZdgkzzXYjKlJTo7-Guxwz4mLYhOSEOLEGWrcA3gp9opmxVh0OdJzmzk5pHWYnifRRABXgh0e86JBCtO3eeNyk5-gFYxqzs_bLb3UWNhmugv38fFj8OQzM-XqoGYm5mIL9bIL7Lmkdrp5oekPSZu6K_G4RQytTH7_XAuK_h2vXc2QOfX_Y1U1r5IEeqtmv6NQw' \
--data-raw '{
	"title": "Less Violent Movie"
}'

```

##### Sample Response

```
{
    "movie": {
        "movie_id": 6,
        "release_date": "2020-07-04",
        "title": "Less Violent Movie"
    },
    "success": true
}
```

#### DELETE /actors/{actor_id} - To delete an existing actor

Deletes an existing actor with the given actor_id (required). Returns the success value and the id of the deleted actor.

##### Sample Request

```
curl --location --request DELETE 'localhost:5000/actors/8' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MDUyMzk5NCwiZXhwIjoxNTgwNjEwMzk0LCJhenAiOiJOMG9IMWI3YW9sWHF0U2pnYzJoS3hGRDZldWx2SlZ0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.dkX2juQeJRWoJmSB8Cn6g3Qra2QiFZwe_Aj_W722CeSXTNBHXpwSFtWSvB7n1_wQR7IcoTUHBIa-y2e-_tj8c2diMhYSkCGz9ffHbrqUPy9at7BLsOe9FW5HhsC2Libhm4rRc7GBNf7EQM8cnzZ1MZdgkzzXYjKlJTo7-Guxwz4mLYhOSEOLEGWrcA3gp9opmxVh0OdJzmzk5pHWYnifRRABXgh0e86JBCtO3eeNyk5-gFYxqzs_bLb3UWNhmugv38fFj8OQzM-XqoGYm5mIL9bIL7Lmkdrp5oekPSZu6K_G4RQytTH7_XAuK_h2vXc2QOfX_Y1U1r5IEeqtmv6NQw'
```

##### Sample Response

```
{
    "delete": 8,
    "success": true
}
```

#### DELETE /movies/{movie_id} - To delete an existing movie

Deletes an existing movie with the given movie_id (required). Returns the success value and the id of the deleted movie.

##### Sample Request

```
curl --location --request DELETE 'localhost:5000/movies/6' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qQkNOMEV5TURkR1JqSXhPRVJFT0RORE9UZzFORGxFTVRBd09USTVOekZCT1RNek1URTFNUSJ9.eyJpc3MiOiJodHRwczovL21jYmNvZmZlZS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUwMGM3MWM2MDhjMWEwZTc3YjY4NWZjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4MDUyMzk5NCwiZXhwIjoxNTgwNjEwMzk0LCJhenAiOiJOMG9IMWI3YW9sWHF0U2pnYzJoS3hGRDZldWx2SlZ0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.dkX2juQeJRWoJmSB8Cn6g3Qra2QiFZwe_Aj_W722CeSXTNBHXpwSFtWSvB7n1_wQR7IcoTUHBIa-y2e-_tj8c2diMhYSkCGz9ffHbrqUPy9at7BLsOe9FW5HhsC2Libhm4rRc7GBNf7EQM8cnzZ1MZdgkzzXYjKlJTo7-Guxwz4mLYhOSEOLEGWrcA3gp9opmxVh0OdJzmzk5pHWYnifRRABXgh0e86JBCtO3eeNyk5-gFYxqzs_bLb3UWNhmugv38fFj8OQzM-XqoGYm5mIL9bIL7Lmkdrp5oekPSZu6K_G4RQytTH7_XAuK_h2vXc2QOfX_Y1U1r5IEeqtmv6NQw'
```

##### Sample Response

```
{
    "delete": 6,
    "success": true
}
```

## Next Steps

This project needs a front end. Fortunately, the author is enrolled in the Udacity Front End Developer Nanodegree program and has plans to complete this soon.

## Authors

Maleina Bidek (maleina@ucla.edu).

Udacity Team. (Some of this readme has been adapted and/or paraphrased from previous project instructions.)

## Acknowledgements

Thanks to the entire Udacity Team, especially to my mentor, Sabrina!
