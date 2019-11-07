from .database import BaseModel


class Book(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    title = AppDb.Column(AppDb.String(80), nullable=False)
    author = AppDb.Column(AppDb.String(80), nullable=False, index=True)
    isbn = AppDb.Column(AppDb.String(40), nullable=False)
    category = AppDb.Column(AppDb.String(100), nullable=True)
    review = AppDb.Column(AppDb.Text, nullable=True)

    def __repr__(self):
        return '<Book Title: {0} \nAuthor: {1} >'.format(self.title, self.author)
