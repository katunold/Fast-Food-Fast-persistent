"""
Module for token model
"""
import datetime

from api.models.database import DatabaseConnection
from api.utils.singleton import Singleton


class TokenModel:
    """
    Model to hold blacklisted tokens
    """

    def __init__(self, token=None):
        self.blacklisted_on = None
        self.token = token


class Tokens(metaclass=Singleton):
    """
    Define token module attributes accessed by callers
    """
    _table_ = "blacklist_token"
    _database_ = DatabaseConnection()

    def blacklist_token(self, token=None):

        token_blacklisted = TokenModel(token)
        token_blacklisted.blacklisted_on = datetime.datetime.now()

        data = {
            'token': token_blacklisted.token,
            'blacklisted_on': token_blacklisted.blacklisted_on
        }
        self._database_.insert(self._table_, data)

        return token_blacklisted

    def check_blacklist(self, auth_token):
        # check whether auth_token has been blacklisted
        criteria = {
            "token": auth_token
        }

        resp = self._database_.find(self._table_, criteria=criteria)

        if resp:
            return True
        else:
            return False
