import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db

'''
CastingTestCase
    This class represents the casting test case.
'''


class CastingTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        database_path = 'postgresql://postgres@localhost:5432/casting_test'
        setup_db(self.app, database_path)

        token = os.environ['TEST_TOKEN']
        bad_token = os.environ['BAD_TOKEN']

        self.header = {
            "Authorization": "Bearer {}".format(token)
        }

        self.bad_header = {
            "Authorization": "Bearer {}".format(bad_token)
        }

        # This is a sample actor to be used during the test
        # of the insertion endpoint.
        self.new_actor = {
            "name": "Joe Smith",
            "birth_date": "November 19, 1992",
            "gender": "M"
        }

        # This is a sample movie to be used during the test
        # of the insertion endpoint.
        self.new_movie = {
            "title": "Big Blockbuster 2021",
            "release_date": "July 4, 2021"
        }

        # This is a sample actor to be used during the test
        # of the patch endpoint.
        self.updated_actor = {
            "name": "Josie D. Smith",
            "birth_date": "November 20, 1992",
            "gender": "F"
        }

        # This is a sample movie to be used during the test
        # of the patch endpoint.
        self.updated_movie = {
            "title": "Bad Movie",
            "release_date": "December 31, 2021"
        }

        # Binds the app to the current context.
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        # Executed after reach test.
        pass

    def test_get_actors(self):
        # Test for successful retrieval of all actors.
        res = self.client().get('/actors', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_404_fail(self):
        # Test fail for get actors at bad endpoint.
        res = self.client().get('/actors1', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actors_401_fail(self):
        # Test fail when do not have 'get:actors' permission
        # ie. not Casting Assistant, Casting Director or Executive Producer.
        res = self.client().get('/actors', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_get_movies(self):
        # Test for successful retrieval of all movies.
        res = self.client().get('/movies', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_movies_404_fail(self):
        # Test fail for get movies at bad endpoint.
        res = self.client().get('/movies1', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies_401_fail(self):
        # Test fail when do not have 'get:movies' permission
        # ie. does not have Casting Assistant, Casting Director or Executive Producer role.
        res = self.client().get('/movies', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_post_new_actor(self):
        # Test for the successful creation of a new actor.
        res = self.client().post('/actors', headers=self.header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_post_new_actor_422_fail(self):
        # Test the failure case for creating a new actor,
        #  ie. bad data passed in request.
        res = self.client().post('/actors', headers=self.header, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_post_new_actor_401_fail(self):
        # Test the failure case when the user doesn't have 'post:actor' permission
        # ie. the user does not have Casting Director or Executive Producer role.
        res = self.client().post('/actors', headers=self.bad_header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_post_new_movie(self):
        # Test for the successful creation of a new movie.
        res = self.client().post('/movies', headers=self.header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_post_new_movie_422_fail(self):
        # Test the failure case for creating a new movie,
        #  ie. bad data passed in request.
        res = self.client().post('/movies', headers=self.header, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_post_new_movie_401_fail(self):
        # Test the failure case when the user doesn't have 'post:movie' permission
        # ie. the user does not have an Executive Producer role.
        res = self.client().post('/movies', headers=self.bad_header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_patch_actor(self):
        # Test for the successful update of an existing actor.
        res = self.client().patch('/actors/1', headers=self.header, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_patch_actor_404_fail(self):
        # Test the failure case for updating an actor,
        #  ie. non-existent actor.
        res = self.client().patch('/actors/500', headers=self.header, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_actor_401_fail(self):
        # Test the failure case when the user doesn't have 'patch:actor' permission
        # ie. the user does not have Casting Director or Executive Producer role.
        res = self.client().patch('/actors/5', headers=self.bad_header, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_patch_movie(self):
        # Test for the successful update of an existing movie.
        res = self.client().patch('/movies/3', headers=self.header, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_patch_movie_404_fail(self):
        # Test the failure case for updating an movie,
        #  ie. non-existent movie.
        res = self.client().patch('/movies/500', headers=self.header, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_movie_401_fail(self):
        # Test the failure case when the user doesn't have 'patch:movie' permission
        # ie. the user does not have Casting Director or Executive Producer role.
        res = self.client().patch('/movies/6', headers=self.bad_header, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_delete_actor(self):
        # Test for the successful deletion of an actor.
        res = self.client().delete('/actors/5', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_404_fail(self):
        # Test for failure when the actor to be deleted
        # doesn't exist.
        res = self.client().delete('/actors/500', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor_401_fail(self):
        # Test for failure when the user doesn't have 'delete:actor' permission
        # ie. the user does not have Casting Director or Executive Producer role.
        res = self.client().delete('/actors/1', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_delete_movie(self):
        # Test for the successful deletion of a movie.
        res = self.client().delete('/movies/2', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_404_fail(self):
        # Test for failure when the movie to be deleted
        # doesn't exist.
        res = self.client().delete('/movies/500', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie_401_fail(self):
        # Test for failure when the user doesn't have 'delete:movie' permission
        # ie. the user does not have an Executive Producer role.
        res = self.client().delete('/movies/2', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')


# Make the tests conveniently executable.
if __name__ == "__main__":
    unittest.main()
