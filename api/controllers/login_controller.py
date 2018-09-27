"""
View module for user login
"""

from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_auth import Authenticate
from api.handlers.return_errors import ReturnError
from api.models.user_model import Users


class LoginController(MethodView):
    """
    User login class with special methods to handle user login
    """
    _user_ = Users()

    def post(self):
        # get post data
        post_data = request.get_json()

        keys = ('user_name', 'password')
        if not set(keys).issubset(set(post_data)):
            return ReturnError.missing_fields(keys)

        try:
            user_name = post_data.get("user_name").strip()
            password = post_data.get("password").strip()
        except AttributeError:
            return ReturnError.invalid_data_type()

        if not user_name or not password:
            return ReturnError.empty_fields()

        user = self._user_.find_user_by_username(user_name)

        if user and Authenticate.verify_password(password, user.password):
            auth_token = Authenticate.encode_auth_token(user.user_id)
            response_object = {
                'status': 'success',
                'message': 'Welcome, You are now logged in',
                'auth_token': auth_token.decode(),
                'logged_in_as': user.user_type
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return jsonify(response_object), 404
