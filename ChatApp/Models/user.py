from ChatApp.Models.database import BaseModel


class User (BaseModel.db.Model):
    AppDb = BaseModel.db
    __tablename__ = 'users'
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    first_name = AppDb.Column(AppDb.String(35), nullable=False)
    last_name = AppDb.Column(AppDb.String(35), nullable=False)
    username = AppDb.Column(AppDb.String(35), nullable=False, unique=True, index=True)
    email = AppDb.Column(AppDb.String(80), nullable=False, index=True)
    password = AppDb.Column(AppDb.String(255), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
