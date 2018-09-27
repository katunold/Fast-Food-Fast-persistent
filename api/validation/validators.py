"""
module to handle user input validation
"""
import re

from api.models.user_model import Users


class Validators:
    """
    Class defines validator functions
    """

    @staticmethod
    def validate_email(email) -> bool:
        """
        Validate email address
        :param email:
        :return:
        """
        pattern = re.compile(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$")
        if not pattern.match(email):
            return False
        return True

    @staticmethod
    def check_if_email_exists(email):
        """
        Check if the email already exists
        :param email:
        :return:
        """
        if Users().find_user_by_email(email):
            return False
        return True

    @staticmethod
    def validate_password(password, length) -> bool:
        """
        password validator
        :param password:
        :param length:
        :return:
        """
        if not isinstance(length, int):
            raise ValueError("length must be an integer")
        if length > len(password):
            return False
        return password.isalnum()

    @staticmethod
    def validate_username(username):
        """
        Username validator
        :param username:
        :return:
        """
        username_regex = re.compile("^[A-Za-z]{4,12}$")
        if not username_regex.match(username):
            return False
        return True

    @staticmethod
    def check_if_user_name_exists(username):
        """
        Check if the username already exists
        :param username:
        :return:
        """
        if Users().find_user_by_username(username):
            return False
        return True

    @staticmethod
    def validate_contact(contact) -> bool:
        """
        Validate contact number. Must be at least 10 digits
        and not more than 13
        :param contact:
        :return:
        """
        if not contact:
            return False

        contact_regex = re.compile("^[0-9]{10,13}$")
        if contact_regex.match(contact):
            return True

        return False

    @staticmethod
    def validate_user_type(user_type: str):
        if user_type.lower() == "admin" or user_type.lower() == "client":
            return True
        return False
