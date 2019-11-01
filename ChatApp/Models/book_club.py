from .database import BaseModel


class BookClub(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    name = AppDb.Column(AppDb.String(80), nullable=False)
    description = AppDb.Column(AppDb.String(255))

    def __repr__(self):
        return '<Book Club {}>'.format(self.name)
