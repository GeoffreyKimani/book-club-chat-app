import os

from ChatApp.constants import DATABASE_URI_ENV_NAME, SECRET_KEY


class BaseConfig(object):
    database_uri = os.getenv(DATABASE_URI_ENV_NAME)
    SQLALCHEMY_DATABASE_URI = database_uri
    SECRET_KEY = os.environ.get(SECRET_KEY) or os.urandom(32)


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ENV = "development"
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "production"
    DEBUG = False
