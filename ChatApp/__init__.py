import os

from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

from ChatApp.constants import APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR, PROD_CONFIG_VAR, APP_NAME
from ChatApp.Models.database import BaseModel
from .Welcome.index_bp import home_bp
from .Authentication.SignUp.signup_bp import signup_bp
from .Authentication.LogIn.login_bp import login_bp
from .ChatArea.chatter_bp import chatter_bp
from .Dashboard.dashboard_bp import dashboard_bp
from .BookClubs.book_club_bp import book_club_bp
from .BookClubBooks.book_club_book import book_club_book_bp


# configure the app
def get_config():
    return os.environ.get(APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR).lower().strip()


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


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(chatter_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(book_club_bp)
    app.register_blueprint(book_club_book_bp)


def create_app():
    app = Flask(__name__)

    # call to configure app and register blue prints
    config_app(app)
    register_blueprints(app)

    # required for form security
    csrf = CSRFProtect(app)
    csrf.init_app(app)
    bcrypt = Bcrypt(app)

    # Database and Migrations setup
    db = BaseModel.init_app(app)

    return app

