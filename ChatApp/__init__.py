import os

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from ChatApp.constants import APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR, PROD_CONFIG_VAR, APP_NAME
from ChatApp.Models.database import BaseModel


# configure the app
def get_config():
    return os.environ.get(APP_CONFIG_ENV_VAR, PROD_CONFIG_VAR).lower().strip()


def config_app(app_instance):
    config_type = get_config()

    # Possible configurations as a dictionary
    configs = {
        DEV_CONFIG_VAR: "ChatApp.config.DevelopmentConfig",
        PROD_CONFIG_VAR: "ChatApp.config.ProductionConfig"
    }

    app_instance.config.from_object(configs[config_type])

    config_file_path = os.environ.get(APP_NAME + "_CONFIG_FILE")

    if config_file_path and os.path.exists(config_file_path):
        app_instance.config.from_pyfile(config_file_path)


# Logging System
def logger(app):
    if not app.debug:
        # TODO: SetUp error messages to be emailed to admin
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/ChatApp.log', maxBytes=1024 * 1024, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Book Club ChatApp')


def register_blueprints(app):
    from .Welcome.index_bp import home_bp
    from .Authentication.SignUp.signup_bp import signup_bp
    from .Authentication.LogIn.login_bp import login_bp
    from .ChatArea.chatter_bp import chatter_bp
    from .Dashboard.dashboard_bp import dashboard_bp
    from .BookClubs.book_club_bp import book_club_bp
    from .BookClubBooks.book_club_book import book_club_book_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(chatter_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(book_club_bp)
    app.register_blueprint(book_club_book_bp)


login = LoginManager()


def create_app():
    app = Flask(__name__)

    login.init_app(app)
    login.login_view = 'login'

    # call to configure app, logging and register blue prints
    config_app(app)

    # Database and Migrations setup
    db = BaseModel.init_app(app)

    logger(app)
    register_blueprints(app)

    # required for form security
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    bcrypt = Bcrypt(app)

    return app

# login = LoginManager()
# login.init_app(app=create_app())
# login.login_view = 'login'


# @login.user_loader
# def load_user(user_id):
#     from ChatApp.Models.user import User
#     return BaseModel.db.session.query(User).get(int(user_id))
