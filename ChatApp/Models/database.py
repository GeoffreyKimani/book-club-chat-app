from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class BaseModel(object):
    db = None

    @staticmethod
    def init_db(app):
        BaseModel.db = SQLAlchemy(app)
        return BaseModel.db

    @staticmethod
    def migrate_db(app, db):
        from .user import User
        from .book_club import BookClub
        Migrate(app, db)

    @staticmethod
    def init_app(app):
        BaseModel.init_db(app)
        BaseModel.migrate_db(app, BaseModel.init_db(app))
