"""
Module handles tests for get orders endpoint
"""
import json
from unittest import TestCase

from api.config.config import TestingConfig
from api.models.database import DatabaseConnection
from run import APP


class TestGetOrderHistory(TestCase):
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

    def login_user(self, user_name=None, password=None):
        return self.client().post(
            '/api/v1/auth/login/',
            data=json.dumps(dict(
                user_name=user_name,
                password=password,
            )),
            content_type='application/json'
        )

    def place_order(self, order_item=None, special_notes=None, token=None):
        return self.client().post(
            '/api/v1/orders',
            headers=dict(
                Authorization='Bearer ' + token
            ),
            data=json.dumps(dict(
                order_item=order_item,
                special_notes=special_notes
            )),
            content_type="application/json"
        )

    # ------------------------- Testing the get order history endpoint ---------------------------------- #

    def test_get_single_order_in_order_history(self):
        """
        Test for getting the the order history
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        self.register_user('Samson', 'sam@gmail.com', '07061806720', 'qwerty', 'Client')

        # user login
        login_admin = self.login_user('Arnold', 'qwerty')
        login_client = self.login_user('Samson', 'qwerty')

        # Add food item
        self.add_food_item("katogo", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", json.loads(login_admin.data.decode())['auth_token'])

        # place order food item
        self.place_order("chappatti and beef", "Please put considerable gravy",
                         json.loads(login_client.data.decode())['auth_token'])

        get_orders = self.client().get(
            '/api/v1/users/orders',
            headers=dict(
                Authorization='Bearer ' + json.loads(login_client.data.decode())['auth_token']
            )
        )

        data = json.loads(get_orders.data.decode())

        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['data'])
        self.assertTrue(get_orders.content_type == 'application/json')
        self.assertEqual(get_orders.status_code, 200)

    def test_get_many_orders_in_order_history(self):
        """
        Test for getting the the order history
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        self.register_user('Samson', 'sam@gmail.com', '07061806720', 'qwerty', 'Client')

        # user login
        login_admin = self.login_user('Arnold', 'qwerty')
        login_client = self.login_user('Samson', 'qwerty')

        # Add food item
        self.add_food_item("katogo", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", json.loads(login_admin.data.decode())['auth_token'])

        # place order food item
        self.place_order("chappatti and beef", "Please put considerable gravy",
                         json.loads(login_client.data.decode())['auth_token'])
        self.place_order("chappatti and beans", "Please put enough soup",
                         json.loads(login_client.data.decode())['auth_token'])
        self.place_order("katogo", "I want katogo of cassava and beans",
                         json.loads(login_client.data.decode())['auth_token'])

        get_orders = self.client().get(
            '/api/v1/users/orders',
            headers=dict(
                Authorization='Bearer ' + json.loads(login_client.data.decode())['auth_token']
            )
        )

        data = json.loads(get_orders.data.decode())

        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['data'])
        self.assertTrue(get_orders.content_type == 'application/json')
        self.assertEqual(get_orders.status_code, 200)

    def test_get_order_history_malformed_bearer_token(self):
        """
        Test for user status with malformed bearer token
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        self.register_user('Samson', 'sam@gmail.com', '07061806720', 'qwerty', 'Client')

        # user login
        login_admin = self.login_user('Arnold', 'qwerty')
        login_client = self.login_user('Samson', 'qwerty')

        # Add food item
        self.add_food_item("katogo", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", json.loads(login_admin.data.decode())['auth_token'])

        # place order food item
        self.place_order("chappatti and beef", "Please put considerable gravy",
                         json.loads(login_client.data.decode())['auth_token'])
        self.place_order("chappatti and beans", "Please put enough soup",
                         json.loads(login_client.data.decode())['auth_token'])
        self.place_order("katogo", "I want katogo of cassava and beans",
                         json.loads(login_client.data.decode())['auth_token'])

        response = self.client().post(
            '/api/v1/orders',
            headers=dict(
                Authorization='Bearer' + json.loads(login_client.data.decode())['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Bearer token malformed')
        self.assertEqual(response.status_code, 401)

    def test_get_order_history_invalid_token(self):
        """
        Test for user status with invalid token
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        self.register_user('Samson', 'sam@gmail.com', '07061806720', 'qwerty', 'Client')

        # user login
        login_admin = self.login_user('Arnold', 'qwerty')
        login_client = self.login_user('Samson', 'qwerty')

        # Add food item
        self.add_food_item("katogo", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", json.loads(login_admin.data.decode())['auth_token'])

        # place order food item
        self.place_order("chappatti and beef", "Please put considerable gravy",
                         json.loads(login_client.data.decode())['auth_token'])
        self.place_order("chappatti and beans", "Please put enough soup",
                         json.loads(login_client.data.decode())['auth_token'])
        self.place_order("katogo", "I want katogo of cassava and beans",
                         json.loads(login_client.data.decode())['auth_token'])

        response = self.client().post(
            '/api/v1/orders',
            headers=dict(
                Authorization='Bearer ' + json.loads(login_client.data.decode())['auth_token'] + 'invalid'
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Invalid token. Please log in again.')
        self.assertEqual(response.status_code, 401)