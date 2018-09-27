"""
Authentication module for JWT token
"""
import datetime

import bcrypt
import jwt

from api.config.config import BaseConfig
from api.models.user_model import Users
from api.utils.singleton import Singleton


class Authenticate(metaclass=Singleton):
    """
    Class defines method used by JWT
    """
    _users_ = Users()

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generate auth token
        :param user_id:
        :return:
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            val = jwt.encode(payload, BaseConfig.SECRET_KEY, algorithm='HS256')
            return val
        except Exception as ex:
            return ex

    @staticmethod
    def hash_password(password):
        """
        method to hash password
        :param password:
        :return:
        """
        try:
            return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt(12))
        except ValueError:
            return False

    @staticmethod
    def verify_password(password_text, hashed):
        """
        verify client password with stored password
        :param password_text:
        :param hashed:
        :return:
        """
        try:
            return bcrypt.checkpw(password_text.encode('utf8'), hashed)
        except ValueError:
            return False
