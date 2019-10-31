from flask_sqlalchemy import SQLAlchemy


class BaseModel(object):
    db = None

    @staticmethod
    def init_db(app):
        BaseModel.db = SQLAlchemy(app)
