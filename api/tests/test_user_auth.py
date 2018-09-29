"""
Module handles all tests
"""
import json
import time
from unittest import TestCase

from api.config.config import TestingConfig
from api.models.database import DatabaseConnection
from api.models.token_model import Tokens
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

    def test_fine_user_registration(self):
        """
        Test for user registration
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', '0706180672', 'qwerty', 'client')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'] == 'success')
        self.assertTrue(received_data['message'] == 'Successfully registered')
        self.assertTrue(received_data['data']['user_type'] == 'client')
        self.assertTrue(register.content_type == 'application/json')
        self.assertEqual(register.status_code, 201)

    def test_fine_admin_registration(self):
        """
        Test for user registration
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', '0706180672', 'qwerty', 'admin')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'] == 'success')
        self.assertTrue(received_data['message'] == 'Successfully registered')
        self.assertTrue(received_data['data']['user_type'] == 'admin')
        self.assertTrue(register.content_type == 'application/json')
        self.assertEqual(register.status_code, 201)

    def test_missing_fields_during_signup(self):
        """
        Test for missing fields during user registration
        :return:
        """
        register = self.client().post(
            '/api/v1/auth/signup/',
            data=json.dumps(dict(
                user_name='Arnold',
                email='arnold@gmail.com',
                contact='0706180670',
                password='qwerty',
            )),
            content_type="application/json"
        )
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "some of these fields are missing")
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_data_type(self):
        """
        Test user registration with invalid data-type
        :return:
        """
        register = self.register_user(13421516, 'arnold@gmail.com', '0706180672', 'qwerty', 'admin')
        received_data = json.loads(register.data.decode())
        self.assertTrue(received_data['status'] == 'fail')
        self.assertTrue(received_data['error_message'] == 'Only string data type supported')
        self.assertFalse(received_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_empty_fields_during_signup(self):
        """
        Test for empty fields during user registration
        :return:
        """
        register = self.register_user(' ', 'arnold@gmail.com', '0706180672', 'qwerty', 'admin')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "some of these fields have empty/no values")
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_password_length(self):
        """
        Test for password less than 6 characters
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', '0706180672', 'qwer', 'admin')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] ==
                        "Password is wrong. It should be at-least 6 characters long, and alphanumeric.")
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_email_registration(self):
        """
        Test for registration with invalid email
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail', '0706180672', 'qwerty', 'admin')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'])
        self.assertTrue(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 400)

    def test_invalid_contact(self):
        """
        testing invalid contact
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', '0706180', 'qwerty', 'admin')
        data = json.loads(register.data.decode())
        self.assertEqual(register.status_code, 400)
        self.assertIn("error_message", data)
        self.assertTrue(data['error_message'])

    def test_invalid_user_name(self):
        """
        testing invalid contact
        :return:
        """
        register = self.register_user('Arnold94', 'arnold@gmail.com', '0706180672', 'qwerty', 'admin')
        data = json.loads(register.data.decode())
        self.assertIn("error_message", data)
        self.assertFalse(data['data'])
        self.assertTrue(data['error_message'])
        self.assertEqual(register.status_code, 400)
        self.assertTrue(register.content_type, 'application/json')

    def test_user_name_exists(self):
        """
        Test when the user name already exists
        :return:
        """
        self.register_user('Arnold', 'arnold94@gmail.com', '0706180672', 'qwerty', 'admin')
        register = self.register_user('Arnold', 'arnold@gmail.com', '0706180672', 'qwerty', 'admin')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "Username already taken")
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 409)

    def test_email_exists(self):
        """
        Test when the user name already exists
        :return:
        """
        self.register_user('Arnold', 'arnold@gmail.com', '0706180672', 'qwerty', 'admin')
        register = self.register_user('Katumba', 'arnold@gmail.com', '0706180672', 'qwerty', 'admin')
        response_data = json.loads(register.data.decode())
        self.assertTrue(response_data['status'] == "fail")
        self.assertTrue(response_data['error_message'] == "email already exists")
        self.assertFalse(response_data['data'])
        self.assertTrue(register.content_type == "application/json")
        self.assertEqual(register.status_code, 409)

    def test_register_with_invalid_user_type(self):
        """
        testing invalid contact
        :return:
        """
        register = self.register_user('Arnold', 'arnold@gmail.com', '0706180672', 'qwerty', 'guest')
        data = json.loads(register.data.decode())
        self.assertIn("error_message", data)
        self.assertTrue(data['data'])
        self.assertTrue(data['error_message'])
        self.assertEqual(register.status_code, 400)
        self.assertTrue(register.content_type, 'application/json')

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
        self.assertTrue(response_data['error_message'] == 'some of these fields are missing')
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
        self.assertTrue(response_data['error_message'] == 'Only string data type supported')
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

        add_food_item = self.client().post(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                food_item="Katogo"
            )),
            content_type="application/json"
        )

        data = json.loads(add_food_item.data.decode())

        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully Added a new food item')
        self.assertEqual(add_food_item.status_code, 201)

    def test_add_menu_item_client(self):
        """
        Test for adding a menu item by the client
        :return:
        """
        # user registration
        self.register_user('Arnold', 'arnold@gmail.com', '07061806720', 'qwerty', 'client')

        # user login
        login = self.login_user('Arnold', 'qwerty')

        add_food_item = self.client().post(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                food_item="Katogo"
            )),
            content_type="application/json"
        )

        data = json.loads(add_food_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Permission denied, Please Login as Admin')
        self.assertEqual(add_food_item.status_code, 403)

    def test_add_menu_item_admin_empty(self):
        """
        Test for adding a menu item with empty fields
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
            data=json.dumps(dict(
                food_item=" "
            )),
            content_type="application/json"
        )

        data = json.loads(add_food_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'some of these fields have empty/no values')
        self.assertTrue(data['data'])
        self.assertTrue(add_food_item.content_type == 'application/json')
        self.assertEqual(add_food_item.status_code, 400)

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

        add_food_item = self.client().post(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                food_item=12313343
            )),
            content_type="application/json"
        )

        data = json.loads(add_food_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'Only string data type supported')
        self.assertFalse(data['data'])
        self.assertTrue(add_food_item.content_type == 'application/json')
        self.assertEqual(add_food_item.status_code, 400)

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
        self.client().post(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                food_item="katogo"
            )),
            content_type="application/json"
        )

        # Add item for the second time
        add_food_item = self.client().post(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                food_item="katogo"
            )),
            content_type="application/json"
        )

        data = json.loads(add_food_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['error_message'] == 'Item already exists')
        self.assertFalse(data['data'])
        self.assertTrue(add_food_item.content_type == 'application/json')
        self.assertEqual(add_food_item.status_code, 409)

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

        add_food_item = self.client().post(
            '/api/v1/menu',
            headers=dict(
                Authorization='Bearer ' + json.loads(login.data.decode())['auth_token']
            ),
            data=json.dumps(dict(
                food_item="Katogo"
            )),
            content_type="application/json"
        )

        data = json.loads(add_food_item.data.decode())

        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Signature expired. Please log in again.')
        self.assertTrue(add_food_item.content_type == 'application/json')
        self.assertEqual(add_food_item.status_code, 401)

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
