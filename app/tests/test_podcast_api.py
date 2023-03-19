import unittest
import json
from app import app, db
from app.models.user_models import User
from app.models.podcast_models import Podcast

class TestPodcastAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db

        with app.app_context():
            self.db.create_all()

    def tearDown(self):
        with app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_create_user(self):
        with app.app_context():
            data = {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpassword'
            }
            response = self.app.post(
                '/api/users/register', data=json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(User.query.count(), 1)

    def authenticate_test_user(self, is_admin=False):
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            if not user:
                user = User(username='testuser',
                            email='test@example.com', is_admin=is_admin)
                user.set_password('testpassword')
                self.db.session.add(user)
                self.db.session.commit()
            else:
                # Reset the password to ensure it matches
                user.set_password('testpassword')
                user.is_admin = is_admin  # Update the is_admin attribute
                self.db.session.commit()

        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.app.post(
            '/api/users/login', data=json.dumps(data), content_type='application/json')
        return json.loads(response.data)["access_token"]

    def test_add_podcast(self):
        with app.app_context():
            access_token = self.authenticate_test_user(
                is_admin=True)  # Set is_admin=True

            data = {
                'title': 'Test Podcast',
                'description': 'This is a test podcast.',
                'author_id': 1,
                'genre_id': 1
            }
            headers = {'Authorization': f'Bearer {access_token}',
                       'Content-Type': 'application/json'}
            response = self.app.post(
                '/api/podcasts', data=json.dumps(data), headers=headers)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(Podcast.query.count(), 1)

    def test_get_all_podcasts(self):
        with app.app_context():
            response = self.app.get('/api/podcasts')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(json.loads(response.data), list))

    def test_get_podcast(self):
        with app.app_context():
            # Create a podcast
            podcast = Podcast(
                title='Test Podcast', description='This is a test podcast.', author_id=1, genre_id=1)
            db.session.add(podcast)
            db.session.commit()

            response = self.app.get(f'/api/podcasts/{podcast.id}')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(json.loads(response.data), dict))

    def test_update_podcast(self):
        with app.app_context():
            access_token = self.authenticate_test_user(is_admin=True)

            # Create a podcast
            podcast = Podcast(
                title='Test Podcast', description='This is a test podcast.', author_id=1, genre_id=1)
            db.session.add(podcast)
            db.session.commit()
            # Add this line to refresh the podcast object
            db.session.refresh(podcast)

            data = {
                'title': 'Updated Test Podcast',
                'description': 'This is an updated test podcast.',
                'genre_id': 2
            }
            headers = {'Authorization': f'Bearer {access_token}',
                       'Content-Type': 'application/json'}
            response = self.app.put(
                f'/api/podcasts/{podcast.id}', data=json.dumps(data), headers=headers)
            self.assertEqual(response.status_code, 200)

            updated_podcast = Podcast.query.get(podcast.id)
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
            response = self.app.delete(
                f'/api/podcasts/{podcast.id}', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(Podcast.query.get(podcast.id))

        # Add more test cases following the same pattern for other routes and resources


if __name__ == '__main__':
    unittest.main()
