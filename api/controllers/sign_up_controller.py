"""
module to handle user sign-up logic
"""
import copy

from flask import request, jsonify
from flask.views import MethodView

from api.auth.user_auth import Authenticate
from api.handlers.return_errors import ReturnError
from api.models.user_model import Users
from api.validation.validators import Validators


class SignUpController(MethodView):
    """
    User Registration
    """
    _user_ = Users()
    validate = Validators()

    def post(self):

        post_data = request.get_json()

        keys = ("user_name", "email", "contact", "password", "user_type")
        if not set(keys).issubset(set(post_data)):
            return ReturnError.missing_fields(keys)
        try:
            user_name = post_data.get('user_name').strip()
            email = post_data.get('email').strip()
            contact = post_data.get('contact').strip()
            password = post_data.get('password').strip()
            user_type = post_data.get('user_type').strip()
        except AttributeError:
            return ReturnError.invalid_data_type()

        if not user_name or not email or not contact or not password or not user_type:
            return ReturnError.empty_fields()
        elif not self.validate.validate_password(password, 6):
            return ReturnError.invalid_password()
        elif not self.validate.validate_email(email):
            return ReturnError.invalid_email()
        elif not self.validate.check_if_email_exists(email):
            return ReturnError.email_already_exists()
        elif not self.validate.validate_contact(contact):
            return ReturnError.invalid_contact()
        elif not self.validate.validate_name(user_name):
            return ReturnError.invalid_name()
        elif not self.validate.check_if_user_name_exists(user_name):
            return ReturnError.username_already_exists()
        elif not self.validate.validate_user_type(user_type):
            return ReturnError.invalid_user_type()
        user = self._user_.register_user(user_name, email, contact,
                                         Authenticate.hash_password(password), user_type.lower())
        user = copy.deepcopy(user)
        del user.password

        response_object = {
            'status': 'success',
            'message': 'Successfully registered',
            'data': user.__dict__
        }
        return jsonify(response_object), 201
