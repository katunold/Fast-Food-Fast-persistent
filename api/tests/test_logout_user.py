"""
Module handles tests for user auth
"""
import json
import time
from unittest import TestCase

from api.config.config import TestingConfig
from api.models.database import DatabaseConnection
from api.models.token_model import Tokens
from run import APP


class TestLogOut(TestCase):
    def setUp(self):
        APP.config.from_object(TestingConfig)
        self.client = APP.test_client
        self.database = DatabaseConnection()
        self.database.init_db(APP)
        self.token = None

    def tearDown(self):
        self.database.drop_test_schema()

    def register_user(self, user_name=None, email=None, contact=None,
                      password=None, user_type=None):
        return self.client().post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                user_name=user_name,
                email=email,
                contact=contact,
                password=password,
                user_type=user_type
            )),
            content_type="application/json"
        )

    def login_user(self, user_name=None, password=None):
        return self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name=user_name,
                password=password,
            )),
            content_type='application/json'
        )

    def test_valid_logout(self):
        """ Test for logout before token expires """

        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        # user login
        login_user = self.login_user('Arnold', 'qwerty')
        # valid token logout
        response = self.client().post(
            '/api/v1/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_user.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged out')
        self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        """ Testing logout after the token expires """

        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        # user login
        login_user = self.login_user('Arnold', 'qwerty')

        # invalid token logout
        time.sleep(6)
        response = self.client().post(
            '/api/v1/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_user.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'Signature expired. Please log in again.')
        self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        """
        Test for logout after a valid token gets blacklisted
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login_user = self.login_user('Arnold', 'qwerty')

        # blacklist a valid token
        Tokens().blacklist_token(token=json.loads(login_user.data.decode())['auth_token'])

        # blacklisted valid token logout
        response = self.client().post(
            '/api/v1/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    login_user.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
        self.assertEqual(response.status_code, 401)

    def test_user_logout_malformed_bearer_token(self):
        """
        Test for user status with malformed bearer token
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login_user = self.login_user('Arnold', 'qwerty')

        response = self.client().post(
            '/api/v1/auth/logout/',
            headers=dict(
                Authorization='Bearer' + json.loads(login_user.data.decode())['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Bearer token malformed')
        self.assertEqual(response.status_code, 401)