"""
Module to return missing fields
"""
from flask import jsonify, request


class ReturnError:
    """
    Class with methods to return specific error messages
    """

    @staticmethod
    def missing_fields(keys):
        return jsonify({"status": "fail",
                        "error_message": "These fields are missing",
                        "data": keys}), 400

    @staticmethod
    def invalid_data_type(data_type, field):
        if data_type == "int":
            response_object = {
                "status": "fail",
                "error_message": "Only {} data type supported for {}".format(data_type, field),
                "data": False}
        else:
            response_object = {
                "status": "fail",
                "error_message": "Only {} data type supported for {}".format(data_type, field),
                "data": False}

        return jsonify(response_object), 400

    @staticmethod
    def empty_fields():
        return jsonify({"status": "fail",
                        "error_message": "some of these fields have empty/no values",
                        "data": request.get_json()}), 400

    @staticmethod
    def invalid_password():
        return jsonify({
            "status": "fail",
            "error_message": "Password is wrong. It should be at-least 6 characters"
                             " long, and alphanumeric.", "data": request.get_json()}), 400

    @staticmethod
    def invalid_email():
        req = request.get_json()
        return jsonify({
            "status": "fail",
            "error_message": "User email {0} is wrong, It should be "
                             "in the format (xxxxx@xxxx.xxx)".format(req['email']),
            "data": req
        }), 400

    @staticmethod
    def invalid_contact():
        return jsonify({"error_message": "Contact {0} is wrong. should be in"
                                         " the form, (070******) and between 10 and 13 "
                                         "digits".format(request.json['contact']),
                        "data": request.json}), 400

    @staticmethod
    def username_already_exists():
        response_object = {
            'status': 'fail',
            'error_message': 'Username already taken',
            'data': False,

        }
        return jsonify(response_object), 409

    @staticmethod
    def email_already_exists():
        response_object = {
            'status': 'fail',
            'error_message': 'email already exists',
            'data': False,

        }
        return jsonify(response_object), 409

    @staticmethod
    def item_already_exists():
        response_object = {
            'status': 'fail',
            'error_message': 'Item already exists',
            'data': False,

        }
        return jsonify(response_object), 409

    @staticmethod
    def item_not_on_the_menu(order_item):
        response_object = {
            'status': 'fail',
            'error_message': 'Sorry, Order item {} not on the menu'.format(order_item)
        }
        return jsonify(response_object), 404

    @staticmethod
    def invalid_name():
        return jsonify({
            "status": "fail",
            "error_message": "A name should consist of only alphabetic characters",
            "data": False
        }), 400

    @staticmethod
    def invalid_user_type():
        req = request.get_json()
        return jsonify({
            "status": "fail",
            "error_message": "User type {0} does not exist ".format(req['user_type']),
            "data": req
        }), 400

    @staticmethod
    def user_bearer_token_error():
        response_object = {
            'status': 'fail',
            'message': 'Bearer token malformed'
        }
        return jsonify(response_object), 401

    @staticmethod
    def invalid_user_token(resp):
        response_object = {
            'status': 'fail',
            'message': resp
        }
        return jsonify(response_object), 401

    @staticmethod
    def denied_permission():
        response_object = {
            'status': 'fail',
            'message': 'Permission denied, Please Login as Admin'
        }
        return jsonify(response_object), 403

    @staticmethod
    def no_items(item):
        response_object = {
            'status': 'successful',
            'message': 'No {} items currently'.format(item)
        }
        return jsonify(response_object), 200

    @staticmethod
    def order_item_absent():
        response_object = {
            'status': 'successful',
            'message': 'Order item not found'
        }
        return jsonify(response_object), 404

    @staticmethod
    def menu_item_absent(item_id):
        response_object = {
            'status': 'fail',
            'message': 'menu item {} not found'.format(item_id)
        }
        return jsonify(response_object), 404

    @staticmethod
    def no_order():
        return jsonify({
            "status": "fail",
            "message": "Order not found",
            "data": False
        }), 404

    @staticmethod
    def order_status_not_found(order_status):
        return jsonify({
            "status": "fail",
            "error_message": "Order status {} not found".format(order_status),
            "data": False}), 404
