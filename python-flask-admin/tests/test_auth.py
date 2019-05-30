# Standard library imports
import unittest
from unittest.mock import patch

# Local application imports
import app
from app.auth.utils import fetch_token, token_expired


class ResponseMock():
    def __init__(self, creds=True, status_code=200):
        self.creds = creds
        self.status_code = status_code

    def json(self):
        return {'access_token': 'some_token'} if self.creds else {'error': 1}


class AuthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.create_app((), testing=True)
        cls.context = cls.app.app_context()
        cls.app.config['CLIENT_ID'] = 'some_id'
        cls.app.config['AUTH_URI'] = 'some_uri'
        cls.username = 'username'
        cls.password = 'password'

    @patch('requests.post', return_value = ResponseMock())
    def test_fetch_token_right_creds(self, value):
        with self.context:
            result = fetch_token(self.username, self.password)
        self.assertDictEqual(result, {'access_token': 'some_token'})

    @patch('requests.post', return_value=ResponseMock(creds=False))
    def test_fetch_token_wrong_creds(self, value):
        with self.context:
            result = fetch_token(self.username, self.password)
        self.assertDictEqual(result, {'error': 1})

    @patch('requests.get', return_value=ResponseMock(status_code=401))
    def test_check_token_expired(self, value):
        with self.context:
            result = token_expired('expired_token')
        self.assertTrue(result)

    @patch('requests.get', return_value=ResponseMock(status_code=200))
    def test_check_token_valid(self, value):
        with self.context:
            result = token_expired('valid_token')
        self.assertFalse(result)





