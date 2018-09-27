"""
Authentication module for JWT token
"""
import bcrypt

from api.models.user_model import Users
from api.utils.singleton import Singleton


class Authenticate(metaclass=Singleton):
    """
    Class defines method used by JWT
    """
    _users_ = Users()

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
