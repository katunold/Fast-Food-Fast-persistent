"""
Module to handle user logout
"""
from flasgger import swag_from
from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_auth import Authenticate
from api.handlers.return_errors import ReturnError
from api.models.token_model import Tokens
from api.validation.validators import Validators


class LogoutController(MethodView):
    """
    Logout class with methods to handle user logout
    """

    @swag_from('../docs/signout.yml')
    def post(self):
        # get auth_token
        auth_header = request.headers.get('Authorization')
        if Validators.check_auth_header(auth_header):
            auth_token = Validators.check_auth_header(auth_header)

            resp = Authenticate.decode_auth_token(auth_token)

            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = Tokens().blacklist_token(auth_token)

                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out',
                    'token_blacklisted': blacklist_token.token
                }
                return jsonify(response_object), 200
            else:
                return ReturnError.invalid_user_token(resp)
        else:
            return ReturnError.user_bearer_token_error()


