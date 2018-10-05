"""
Module handles tests for user auth
"""
import json
from unittest import TestCase

from api.config.config import TestingConfig
from api.models.database import DatabaseConnection
from run import APP


class TestUserAuth(TestCase):
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

    # ------------------------- Testing the update order status endpoint ---------------------------------- #

    def test_update_order_status_client(self):
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

        update_order = self.client().put(
            '/api/v1/orders/2/',
            headers=dict(
                Authorization='Bearer ' + json.loads(login_client.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                order_status="Processing"
            )),
            content_type='application/json'
        )

        data = json.loads(update_order.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Permission denied, Please Login as Admin')
        self.assertTrue(update_order.content_type == 'application/json')
        self.assertEqual(update_order.status_code, 403)

    def test_update_order_status_malformed_bearer_token(self):
        """
        Test for updating the order with malformed bearer token
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

        update_order = self.client().put(
            '/api/v1/orders/2/',
            headers=dict(
                Authorization='Bearer' + json.loads(login_admin.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                order_status="Processing"
            )),
            content_type='application/json'
        )

        data = json.loads(update_order.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Bearer token malformed')
        self.assertTrue(update_order.content_type == 'application/json')
        self.assertEqual(update_order.status_code, 401)

    def test_update_order_status_invalid_bearer_token(self):
        """
        Test for updating the order with malformed bearer token
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

        update_order = self.client().put(
            '/api/v1/orders/2/',
            headers=dict(
                Authorization='Bearer ' + json.loads(login_admin.data.decode())['auth_token'] + 'invalid'
            ),
            data=json.dumps(dict(
                order_status="Processing"
            )),
            content_type='application/json'
        )

        data = json.loads(update_order.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Invalid token. Please log in again.')
        self.assertEqual(update_order.status_code, 401)

    def test_user_post_malformed_bearer_token(self):
        """
        Test for user status with malformed bearer token
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login_user = self.login_user('Arnold', 'qwerty')

        response = self.client().post(
            '/api/v1/orders',
            headers=dict(
                Authorization='Bearer' + json.loads(login_user.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                order_item="Mbuzi",
                special_notes=""
            )),
            content_type="application/json"
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Bearer token malformed')
        self.assertEqual(response.status_code, 401)
