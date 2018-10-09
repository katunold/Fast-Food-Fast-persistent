"""
Module to handle menu logic
"""
from flasgger import swag_from
from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_auth import Authenticate
from api.handlers.return_errors import ReturnError
from api.models.food_item_model import FoodItems
from api.validation.validators import Validators


class MenuController(MethodView):
    """
    Class has special methods to handle menu logic
    """
    food_item = None
    price = None
    validate = Validators()
    auth = Authenticate
    food_model = FoodItems()

    @swag_from('../docs/add_menu_item.yml')
    def post(self):
        """
        Method to post a menu item
        :return:
        """

        # get auth_token
        auth_header = request.headers.get('Authorization')
        if self.validate.check_auth_header(auth_header):
            auth_token = self.validate.check_auth_header(auth_header)

            resp = self.auth.decode_auth_token(auth_token)

            if not isinstance(resp, str):

                if self.validate.check_user_type(resp):
                    post_data = request.get_json()

                    key = ["food_item", "price"]

                    if not set(key).issubset(set(post_data)):
                        return ReturnError.missing_fields([item for item in key if item not in post_data])
                    try:
                        self.food_item = post_data['food_item'].strip()
                    except AttributeError:
                        return ReturnError.invalid_data_type('string', key[0])
                    try:
                        self.price = int(post_data['price'])
                    except ValueError:
                        return ReturnError.invalid_data_type('int', key[1])

                    if not self.food_item or not self.price:
                        return ReturnError.empty_fields()
                    elif not self.validate.validate_name(self.food_item):
                        return ReturnError.invalid_name()
                    elif self.validate.check_item_name(self.food_item.lower()):
                        return ReturnError.item_already_exists()

                    food_data = self.food_model.add_food_item(self.food_item.lower(), resp, self.price)

                    response_object = {
                        'status': 'success',
                        'message': 'Successfully Added a new food item',
                        'data': food_data.__dict__
                    }
                    return jsonify(response_object), 201
                return ReturnError.denied_permission()
            else:
                return ReturnError.invalid_user_token(resp)
        else:
            return ReturnError.user_bearer_token_error()

    @swag_from('../docs/view_menu_items.yml')
    def get(self):
        """
        Method to return existing menu items
        :return:
        """

        # get auth_token
        auth_header = request.headers.get('Authorization')

        if self.validate.check_auth_header(auth_header):
            auth_token = self.validate.check_auth_header(auth_header)

            resp = self.auth.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                menu_data = self.food_model.get_menu()

                if menu_data:
                    if isinstance(menu_data, list) and len(menu_data) > 0:
                        response_object = {
                            "status": "successful",
                            "data": [obj.__dict__ for obj in menu_data]
                        }
                        return jsonify(response_object), 200
                    elif isinstance(menu_data, object):

                        response_object = {
                            "status": "successful",
                            "data": [menu_data.__dict__]
                        }
                        return jsonify(response_object), 200
                else:
                    return ReturnError.no_items('menu')
            else:
                return ReturnError.invalid_user_token(resp)
        else:
            return ReturnError.user_bearer_token_error()

    @swag_from('../docs/delete_menu_item.yml')
    def delete(self, item_id):
        """
        responds to delete requests
        :param item_id:
        :return:
        """

        # get auth_token
        auth_header = request.headers.get('Authorization')

        if self.validate.check_auth_header(auth_header):
            auth_token = self.validate.check_auth_header(auth_header)

            resp = self.auth.decode_auth_token(auth_token)

            if not isinstance(resp, str):
                if self.validate.check_user_type(resp):
                    menu_item = self.food_model.find_item_by_id(item_id)

                    if not menu_item:
                        return ReturnError.menu_item_absent(item_id)
                    else:
                        self.food_model.delete_menu_item(item_id)
                        response_object = {
                            "status": "success",
                            "message": "Menu item {0} has been deleted.".format(item_id),
                            "data": True}
                        return jsonify(response_object), 200

                return ReturnError.denied_permission()
            else:
                return ReturnError.invalid_user_token(resp)
        else:
            return ReturnError.user_bearer_token_error()