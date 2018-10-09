"""
Module handles tests for post order endpoint
"""
import json
import time
from unittest import TestCase

from api.config.config import TestingConfig
from api.models.database import DatabaseConnection
from run import APP


class TestPostOrder(TestCase):
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

    def add_food_item(self, item_name=None, price=None, token=None):
        return self.client().post(
            '/api/v1/menu/',
            headers=dict(
                Authorization='Bearer ' + token
            ),
            data=json.dumps(dict(
                food_item=item_name,
                price=price
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

    # ------------------------- Testing the place order endpoint ---------------------------------- #

    def test_place_order_that_is_on_menu(self):
        """
        Test for placing an order that is on the menu
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", 1500, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", 5000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", 1000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", 2000, json.loads(login.data.decode())['auth_token'])

        # place order food item
        order = self.place_order("chappatti and beef", "Please put considerable gravy",
                                 json.loads(login.data.decode())['auth_token'])

        data = json.loads(order.data.decode())

        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully posted an order')
        self.assertTrue(data['data'])
        self.assertTrue(order.content_type == 'application/json')
        self.assertEqual(order.status_code, 201)

    def test_place_order_with_missing_fields(self):
        """
        Test for placing an order with missing fields
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", 1500, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", 5000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", 1000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", 2000, json.loads(login.data.decode())['auth_token'])

        # place order food item
        order = self.client().post(
            '/api/v1/orders/',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                order_item="chappatti and beans"
            )),
            content_type="application/json"
        )

        data = json.loads(order.data.decode())

        print(data)

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'These fields are missing')
        self.assertTrue(data['data'])
        self.assertTrue(order.content_type == 'application/json')
        self.assertEqual(order.status_code, 400)

    def test_place_order_with_invalid_data_type_order_item(self):
        """
        Test for placing an order with invalid data
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", 1500, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", 5000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", 1000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", 2000, json.loads(login.data.decode())['auth_token'])

        # place order food item
        order = self.place_order(5252644268624, "Please put considerable gravy",
                                 json.loads(login.data.decode())['auth_token'])

        data = json.loads(order.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'Only string data type supported for order_item')
        self.assertFalse(data['data'])
        self.assertTrue(order.content_type == 'application/json')
        self.assertEqual(order.status_code, 400)

    def test_place_order_with_invalid_data_type_special_notes(self):
        """
        Test for placing an order with invalid data
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", 1500, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", 5000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", 1000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", 2000, json.loads(login.data.decode())['auth_token'])

        # place order food item
        order = self.place_order('katogo', 2132242542,
                                 json.loads(login.data.decode())['auth_token'])

        data = json.loads(order.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'Only string data type supported for special_notes')
        self.assertFalse(data['data'])
        self.assertTrue(order.content_type == 'application/json')
        self.assertEqual(order.status_code, 400)

    def test_place_order_with_empty_order_item(self):
        """
        Test for placing an order with empty data fields
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", 1500, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", 5000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", 1000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", 2000, json.loads(login.data.decode())['auth_token'])

        # place order food item
        order = self.place_order("", "Please put considerable gravy",
                                 json.loads(login.data.decode())['auth_token'])

        data = json.loads(order.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'some of these fields have empty/no values')
        self.assertTrue(data['data'])
        self.assertTrue(order.content_type == 'application/json')
        self.assertEqual(order.status_code, 400)

    def test_place_order_with_no_special_notes(self):
        """
        Test for placing an order with empty data fields
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", 1500, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", 5000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", 1000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", 2000, json.loads(login.data.decode())['auth_token'])

        # place order food item
        order = self.place_order("Katogo", "Please put considerable gravy",
                                 json.loads(login.data.decode())['auth_token'])

        data = json.loads(order.data.decode())

        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully posted an order')
        self.assertTrue(data['data'])
        self.assertTrue(order.content_type == 'application/json')
        self.assertEqual(order.status_code, 201)

    def test_place_order_not_on_menu(self):
        """
        Test for placing an order with empty data fields
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", 1500, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", 5000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", 1000, json.loads(login.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", 2000, json.loads(login.data.decode())['auth_token'])

        # place order food item
        order = self.place_order("Beef", "Please put considerable gravy",
                                 json.loads(login.data.decode())['auth_token'])

        data = json.loads(order.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'Sorry, Order item beef not on the menu')
        self.assertTrue(order.content_type == 'application/json')
        self.assertEqual(order.status_code, 404)

    def test_invalid_post_order(self):
        """ Testing logout after the token expires """

        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')
        # user login
        login_user = self.login_user('Arnold', 'qwerty')

        # invalid token logout
        time.sleep(6)
        # place order food item
        order = self.place_order("Beef", "Please put considerable gravy",
                                 json.loads(login_user.data.decode())['auth_token'])
        data = json.loads(order.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'Signature expired. Please log in again.')
        self.assertEqual(order.status_code, 401)


