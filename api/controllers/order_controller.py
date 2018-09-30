"""
Module to handle menu logic
"""
from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_auth import Authenticate
from api.handlers.return_errors import ReturnError
from api.models.food_item_model import FoodItems
from api.models.order_model import Orders
from api.validation.validators import Validators


class OrderController(MethodView):
    """
    Class has special methods to handle menu logic
    """

    order_item = None
    special_notes = None
    validate = Validators()
    auth = Authenticate
    menu = FoodItems()
    orders = Orders()

    def post(self):
        """
        Method to post an order
        :return:
         """
        # get auth_token
        auth_header = request.headers.get('Authorization')

        if self.validate.check_auth_header(auth_header):
            auth_token = self.validate.check_auth_header(auth_header)

            resp = self.auth.decode_auth_token(auth_token)

            if not isinstance(resp, str):
                post_data = request.get_json()

                key = ('order_item', 'special_notes')

                if not set(key).issubset(set(post_data)):
                    return ReturnError.missing_fields(key)

                try:
                    self.order_item = post_data['order_item'].strip()
                    self.special_notes = post_data['special_notes'].strip()
                except AttributeError:
                    return ReturnError.invalid_data_type()
                if not self.special_notes:
                    self.special_notes = "No special notes attached"

                if not self.order_item:
                    return ReturnError.empty_fields()
                elif not self.validate.check_item_name(self.order_item):
                    return ReturnError.item_not_on_the_menu(self.order_item.lower())

                order = self.orders.make_order(resp, self.order_item.lower(), self.special_notes)

                response_object = {
                    'status': 'success',
                    'message': 'Successfully posted an order',
                    'data': order.__dict__
                }
                return jsonify(response_object), 201

            else:
                return ReturnError.invalid_user_token(resp)
        else:
            return ReturnError.user_bearer_token_error()

    def get(self, order_id=None):
        """
        Method to return all existing orders
        :return:
        """

        # get auth_token
        auth_header = request.headers.get('Authorization')
        if self.validate.check_auth_header(auth_header):
            auth_token = self.validate.check_auth_header(auth_header)

            resp = self.auth.decode_auth_token(auth_token)

            if not isinstance(resp, str):

                if self.validate.check_user_type(resp):
                    """
                    if order_id:
                        if self.orders.find_order_by_id(order_id):
                            pass
                    """

                    current_orders = self.orders.get_orders()

                    if current_orders:
                        if isinstance(current_orders, list) and len(current_orders) > 0:
                            response_object = {
                                "status": "success",
                                "data": [obj.__dict__ for obj in current_orders]
                            }
                            return jsonify(response_object), 200
                        elif isinstance(current_orders, object):

                            response_object = {
                                "status": "success",
                                "data": [current_orders.__dict__]
                            }
                            return jsonify(response_object), 200
                    else:
                        return ReturnError.no_items('order')

                return ReturnError.denied_permission()
            else:
                return ReturnError.invalid_user_token(resp)
        else:
            return ReturnError.user_bearer_token_error()