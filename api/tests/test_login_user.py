"""
Test user login module
"""

import json
from unittest import TestCase

from api.config.config import TestingConfig
from api.models.database import DatabaseConnection
from run import APP


class TestUserLogin(TestCase):
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

    def test_for_proper_registered_user_login(self):
        """
        Test for proper registered user login
        :return:
        """
        self.register_user('Arnold', 'arnold@gmail.com', '0706180672', 'qwerty', 'Admin')
        login_user = self.login_user('Arnold', 'qwerty')

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'] == 'success')
        self.assertTrue(response_data['message'] == 'Welcome, You are now logged in')
        self.assertTrue(response_data['auth_token'])
        self.assertTrue(response_data['logged_in_as'] == 'admin')
        self.assertTrue(login_user.content_type == 'application/json')
        self.assertEqual(login_user.status_code, 200)

    def test_non_registered_user_login(self):
        """
        Test for login of a non registered user
        :return:
        """
        login_user = self.login_user('Arnold', 'qwerty')
        data = json.loads(login_user.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'User does not exist.')
        self.assertTrue(login_user.content_type == 'application/json')
        self.assertEqual(login_user.status_code, 404)

    def test_login_with_missing_fields(self):
        """
        Test for login with missing fields
        :return:
        """
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        login_user = self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name="Arnold"
            )),
            content_type='application/json'
        )

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'] == 'fail')
        self.assertTrue(response_data['error_message'] == 'These fields are missing')
        self.assertTrue(login_user.content_type == 'application/json')
        self.assertEqual(login_user.status_code, 400)

    def test_login_with_invalid_data_types(self):
        """
        Test for login with invalid data types
        :return:
        """
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        login_user = self.login_user('Arnold', 2334445454)

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'] == 'fail')
        self.assertTrue(response_data['error_message'] == 'Only string data type supported for all fields')
        self.assertTrue(login_user.content_type == 'application/json')
        self.assertEqual(login_user.status_code, 400)

    def test_login_with_empty_fields(self):
        """
        Test for login with empty fields
        :return:
        """
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        login_user = self.login_user('Arnold', '')

        response_data = json.loads(login_user.data.decode())

        self.assertTrue(response_data['status'] == 'fail')
        self.assertTrue(response_data['error_message'] == 'some of these fields have empty/no values')
        self.assertTrue(login_user.content_type == 'application/json')
        self.assertEqual(login_user.status_code, 400)