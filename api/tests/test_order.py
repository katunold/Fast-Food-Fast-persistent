"""
Module handles tests for get items menu routes
"""
import json
from unittest import TestCase

from api.config.config import TestingConfig
from api.models.database import DatabaseConnection
from run import APP


class TestOrder(TestCase):

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

    # ------------------------- Testing the Get menu endpoint ---------------------------------- #

    def test_get_menu(self):
        """
        Test for get menu items
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", json.loads(login.data.decode())['auth_token'])

        get_menu = self.client().get(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            )
        )

        data = json.loads(get_menu.data.decode())

        self.assertTrue(data['status'] == 'successful')
        self.assertTrue(data['data'])
        self.assertTrue(get_menu.content_type == 'application/json')
        self.assertEqual(get_menu.status_code, 200)

    def test_get_menu_with_more_than_one_item(self):
        """
        Test for get menu items
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", json.loads(login.data.decode())['auth_token'])
        self.add_food_item("Pork", json.loads(login.data.decode())['auth_token'])

        get_menu = self.client().get(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            )
        )

        data = json.loads(get_menu.data.decode())

        self.assertTrue(data['status'] == 'successful')
        self.assertTrue(data['data'])
        self.assertTrue(get_menu.content_type == 'application/json')
        self.assertEqual(get_menu.status_code, 200)

    def test_get_empty_menu(self):
        """
        Test for get menu items
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        get_menu = self.client().get(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            )
        )

        data = json.loads(get_menu.data.decode())

        self.assertTrue(data['status'] == 'successful')
        self.assertTrue(data['message'] == 'No menu items currently')
        self.assertTrue(get_menu.content_type == 'application/json')
        self.assertEqual(get_menu.status_code, 200)

