"""
Module contains all global constants
"""
import os


class HostConfig:
    """
    System HOST configuration settings
    They can be changed at any time.
    """
    HOST = "0.0.0.0"
    PORT = 5000


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.urandom(24).hex()
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    HOST = "127.0.0.1"  # ec2-23-23-80-20.compute-1.amazonaws.com
    PORT = "5432"
    DATABASE = "Fast-Food"  # dc09id3sq3n8v9
    USER = "postgres"  # nnmmzuxramdvkg
    PASSWORD = "qwerty"  # b66b5c6610aa107101f45b1ed65fdf579d28336eede8595b3aca8ceed17c6bae


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SCHEMA_PRODUCTION = "production"


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SCHEMA_TESTING = "test"


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SCHEMA_PRODUCTION = "production"




