from main import app
import unittest


class TestApp(unittest.TestCase):

    app_ = app.test_client()

    def default_test(self, url, string, method='GET', status_expected=200, data={}):
        if (method == 'POST'):
            self.response = self.app_.post(url, data=data)
        else:
            self.response = self.app_.get(url)
        self.assertEqual(status_expected, self.response.status_code)
        self.assertIn(string, self.response.data.decode('utf-8'))
        self.assertIn('text/html', self.response.content_type)

    def test_signin(self):
        url = 'signin'
        string = 'SignIn'
        self.default_test(url, string)

    def test_signup(self):
        url = 'signup'
        string = 'SignUp'
        self.default_test(url, string)

    def test_logout(self):
        url = 'logout'
        string = ''
        self.default_test(url, string, status_expected=302)  # redirect code

    def test_auth(self):
        url = 'auth'
        string = ''
        data = {
            "username": 'admin',
            "password": 'admin'
        }
        self.default_test(url, string, method='POST', status_expected=302, data=data)  # redirect code

    def test_create(self):
        url = 'create'
        string = ''
        data = {
            "username": 'admin',
            "password": 'admin'
        }
        self.default_test(url, string, method='POST', status_expected=302, data=data)  # redirect code

    def test_send(self):
        url = 'send'
        string = ''
        data = {
            "message": 'message'
        }
        self.default_test(url, string, method='POST', status_expected=302, data=data)  # redirect code

