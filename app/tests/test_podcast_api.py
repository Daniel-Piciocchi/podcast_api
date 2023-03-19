import unittest
import json
from app import app, db
from app.models.user_models import User
from app.models.podcast_models import Podcast

class TestPodcastAPI(unittest.TestCase):

    def setUp(self):
        # Initialize the Flask test client and the database object
        self.app = app.test_client()
        self.db = db

        # Create all tables in the database
        with app.app_context():
            self.db.create_all()

    def tearDown(self):
        # Remove all sessions from the database and drop all tables
        with app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_create_user(self):
        # Test creating a new user through the API
        with app.app_context():
            # Define the user data to be posted to the API
            data = {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpassword'
            }
            # Make a POST request to the user registration endpoint
            response = self.app.post(
                '/api/users/register', data=json.dumps(data), content_type='application/json')
            # Check that the response status code is 201 (created)
            self.assertEqual(response.status_code, 201)
            # Check that the number of users in the database is now 1
            self.assertEqual(User.query.count(), 1)

    def authenticate_test_user(self, is_admin=False):
        # Helper method to authenticate a test user and retrieve an access token
        with app.app_context():
            # Retrieve the test user from the database
            user = User.query.filter_by(username='testuser').first()
            # If the user does not exist, create a new user
            if not user:
                user = User(username='testuser',
                            email='test@example.com', is_admin=is_admin)
                user.set_password('testpassword')
                self.db.session.add(user)
                self.db.session.commit()
            # Otherwise, update the user's password and is_admin attribute
            else:
                user.set_password('testpassword')
                user.is_admin = is_admin
                self.db.session.commit()

        # Make a POST request to the user login endpoint to retrieve an access token
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.app.post(
            '/api/users/login', data=json.dumps(data), content_type='application/json')
        return json.loads(response.data)["access_token"]

    def test_add_podcast(self):
        # Test adding a new podcast through the API
        with app.app_context():
            # Authenticate a test user with is_admin=True and retrieve an access token
            access_token = self.authenticate_test_user(is_admin=True)

            # Define the podcast data to be posted to the API
            data = {
                'title': 'Test Podcast',
                'description': 'This is a test podcast.',
                'author_id': 1,
                'genre_id': 1
            }
            # Make a POST request to the podcasts endpoint with the access token in the headers
            headers = {'Authorization': f'Bearer {access_token}',
                       'Content-Type': 'application/json'}
            response = self.app.post(
                '/api/podcasts', data=json.dumps(data), headers=headers)
            # Check that the response status code is 201 (created)
            self.assertEqual(response.status_code, 201)
            # Check that the number of podcasts in the database is now 1
            self.assertEqual(Podcast.query.count(), 1)

    def test_get_all_podcasts(self):
        with app.app_context():
            # Send a GET request to the '/api/podcasts' endpoint
            response = self.app.get('/api/podcasts')
            # Assert that the response status code is 200
            self.assertEqual(response.status_code, 200)
            # Assert that the response data is a list
            self.assertTrue(isinstance(json.loads(response.data), list))


    def test_get_podcast(self):
        with app.app_context():
            # Create a podcast
            podcast = Podcast(
                title='Test Podcast', description='This is a test podcast.', author_id=1, genre_id=1)
            db.session.add(podcast)
            db.session.commit()

            # Send a GET request to the '/api/podcasts/{podcast_id}' endpoint
            response = self.app.get(f'/api/podcasts/{podcast.id}')
            # Assert that the response status code is 200
            self.assertEqual(response.status_code, 200)
            # Assert that the response data is a dictionary
            self.assertTrue(isinstance(json.loads(response.data), dict))


    def test_update_podcast(self):
        with app.app_context():
            access_token = self.authenticate_test_user(is_admin=True)

            # Create a podcast
            podcast = Podcast(
                title='Test Podcast', description='This is a test podcast.', author_id=1, genre_id=1)
            db.session.add(podcast)
            db.session.commit()
            # Refresh the podcast object to ensure that we have the latest version
            db.session.refresh(podcast)

            data = {
                'title': 'Updated Test Podcast',
                'description': 'This is an updated test podcast.',
                'genre_id': 2
            }
            headers = {'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'}
            # Send a PUT request to the '/api/podcasts/{podcast_id}' endpoint
            response = self.app.put(
                f'/api/podcasts/{podcast.id}', data=json.dumps(data), headers=headers)
            # Assert that the response status code is 200
            self.assertEqual(response.status_code, 200)

            # Get the updated podcast from the database
            updated_podcast = Podcast.query.get(podcast.id)
            # Assert that the updated podcast has the expected values
            self.assertEqual(updated_podcast.title, data["title"])
            self.assertEqual(updated_podcast.description, data["description"])
            self.assertEqual(updated_podcast.genre_id, data["genre_id"])


    def test_delete_podcast(self):
        with app.app_context():
            access_token = self.authenticate_test_user(is_admin=True)

            # Create a podcast
            podcast = Podcast(
                title='Test Podcast', description='This is a test podcast.', author_id=1, genre_id=1)
            db.session.add(podcast)
            db.session.commit()

            headers = {'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'}
            # Send a DELETE request to the '/api/podcasts/{podcast_id}' endpoint
            response = self.app.delete(
                f'/api/podcasts/{podcast.id}', headers=headers)
            # Assert that the response status code is 200
            self.assertEqual(response.status_code, 200)
            # Assert that the podcast was deleted from the database
            self.assertIsNone(Podcast.query.get(podcast.id))


    


if __name__ == '__main__':
    unittest.main()
