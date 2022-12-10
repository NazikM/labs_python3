import unittest

from flask_testing import TestCase, LiveServerTestCase
from flask_login import login_user, logout_user, current_user
from app import create_app, db
from app.auth.models import User


class BaseTest(TestCase):
    def create_app(self):
        return create_app(config_name='test')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


# class SecondTest(BaseTest, LiveServerTestCase):
#     def test_server_is_up_and_running(self):
#         response = urllib.request.urlopen(self.get_server_url())
#         self.assertEqual(response.code, 200)

class ViewTest(BaseTest):
    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)

    def test_index(self):
        response = self.client.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'About2', response.data)
        assert b'About' in response.data

    def test_user(self):
        user = User(username='test', email='test@test.com', password='1111111')
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email='test@test.com').first()
        assert user.username == 'test'

        login_user(user)

        assert current_user.is_authenticated == True
        logout_user()
        assert current_user.is_authenticated == False
    
    def test_post(self):
        with self.client:
            response = self.client.post(
                    '/auth/register',
                    data=dict(username="test", email="test.user123@gmail.com", password="password1"),
                    follow_redirects=True
                )
        # self.assertEqual(response.status_code, 200)
        # self.assertIn('created', response.data)
        user = User.query.filter_by(email='test.user123@gmail.com').first()
        assert user.username == 'test'
    # def test_is_account_route_to_login(self):
    #     response = self.client.get('/auth/account', follow_redirects=True)
    #     self.assertRedirects(response, 'http://localhost:5000/')
        # self.assertIn(b'Login', response.data)


if __name__ == '__main__':
    unittest.main()
