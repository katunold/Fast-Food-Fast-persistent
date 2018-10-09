"""
Module to test deleting a menu item by the admin
"""
import json
from unittest import TestCase

from api.config.config import TestingConfig
from api.models.database import DatabaseConnection
from run import APP


class TestDeleteMenuItem(TestCase):
    def setUp(self):
        APP.config.from_object(TestingConfig)
        self.client = APP.test_client
        self.database = DatabaseConnection()
        self.database.init_db(APP)
        self.token = None

    def tearDown(self):
        self.database.drop_test_schema()

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

    # ------------------------- Testing the Delete menu item endpoint ---------------------------------- #

    def test_delete_menu_item(self):
        """
        method to test for deleting a menu item
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'Admin')

        # user login
        login_admin = self.login_user('Arnold', 'qwerty')

        # Add food item
        self.add_food_item("katogo", 1500, json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("Fish fillet", 5000, json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beans", 1000, json.loads(login_admin.data.decode())['auth_token'])
        self.add_food_item("chappatti and beef", 2000, json.loads(login_admin.data.decode())['auth_token'])

        del_item = self.client().delete(
            '/api/v1/menu/3/',
            headers=dict(
                Authorization='Bearer ' + json.loads(login_admin.data.decode())['auth_token']
            ),
            content_type='application/json'
        )

        data = json.loads(del_item.data.decode())

        self.assertTrue(data['status'] == "successful")
        self.assertTrue(data['message'] == 'menu item 3 not found')
