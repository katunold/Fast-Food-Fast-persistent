"""
Module handles tests for menu routes
"""
import json
import time
from unittest import TestCase

from api.config.config import TestingConfig
from api.models.database import DatabaseConnection
from run import APP


class TestUserMenu(TestCase):
    def setUp(self):
        APP.config.from_object(TestingConfig)
        self.client = APP.test_client
        self.database = DatabaseConnection()
        self.database.init_db(APP)
        self.token = None

    def tearDown(self):
        self.database.drop_test_schema()

    def add_food_item(self, item_name=None, token=None):
        return self.client().post(
            '/api/v1/menu/',
            headers=dict(
                Authorization='Bearer ' + token
            ),
            data=json.dumps(dict(
                food_item=item_name
            )),
            content_type="application/json"
        )

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

    # ------------------------- Testing the Add menu endpoint ---------------------------------- #

    def test_add_menu_item_admin(self):
        """
        Test for adding a menu item by the admin
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        add_item = self.add_food_item("Katogo", json.loads(login.data.decode())['auth_token'])

        data = json.loads(add_item.data.decode())

        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully Added a new food item')
        self.assertEqual(add_item.status_code, 201)

    def test_add_menu_item_client(self):
        """
        Test for adding a menu item by the client
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'client')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        add_item = self.add_food_item("Katogo", json.loads(login.data.decode())['auth_token'])

        data = json.loads(add_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Permission denied, Please Login as Admin')
        self.assertEqual(add_item.status_code, 403)

    def test_add_menu_item_admin_empty(self):
        """
        Test for adding a menu item with empty fields
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        add_item = self.add_food_item(" ", json.loads(login.data.decode())['auth_token'])

        data = json.loads(add_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'some of these fields have empty/no values')
        self.assertTrue(data['data'])
        self.assertTrue(add_item.content_type == 'application/json')
        self.assertEqual(add_item.status_code, 400)

    def test_add_menu_item_admin_missing(self):
        """
        Test for adding a menu item with missing fields
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        add_food_item = self.client().post(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            ),
            data=json.dumps(dict()),
            content_type="application/json"
        )

        data = json.loads(add_food_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'some of these fields are missing')
        self.assertTrue(data['data'])
        self.assertTrue(add_food_item.content_type == 'application/json')
        self.assertEqual(add_food_item.status_code, 400)

    def test_add_menu_item_admin_data_type(self):
        """
        Test for adding a menu item with wrong data type fields
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        add_item = self.add_food_item(12345456, json.loads(login.data.decode())['auth_token'])

        data = json.loads(add_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'Only string data type supported')
        self.assertFalse(data['data'])
        self.assertTrue(add_item.content_type == 'application/json')
        self.assertEqual(add_item.status_code, 400)

    def test_add_menu_item_admin_item_exists(self):
        """
        Test for adding a menu item with wrong data type fields
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add item for the first time
        self.add_food_item("Katogo", json.loads(login.data.decode())['auth_token'])

        # Add food item
        add_item = self.add_food_item("katogo", json.loads(login.data.decode())['auth_token'])

        data = json.loads(add_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'Item already exists')
        self.assertFalse(data['data'])
        self.assertTrue(add_item.content_type == 'application/json')
        self.assertEqual(add_item.status_code, 409)

    def test_add_menu_item_admin_token_expired(self):
        """
        Test for adding a menu item when token expired
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # token expires
        time.sleep(6)

        # Add food item
        add_item = self.add_food_item("katogo", json.loads(login.data.decode())['auth_token'])

        data = json.loads(add_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Signature expired. Please log in again.')
        self.assertTrue(add_item.content_type == 'application/json')
        self.assertEqual(add_item.status_code, 401)

    def test_add_menu_item_admin_malformed_token(self):
        """
        Test for adding a menu item when token is malformed
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        add_food_item = self.client().post(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer' + json.loads(login.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                food_item="Katogo"
            )),
            content_type="application/json"
        )

        data = json.loads(add_food_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Bearer token malformed')
        self.assertTrue(add_food_item.content_type == 'application/json')
        self.assertEqual(add_food_item.status_code, 401)
