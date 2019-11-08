from .database import BaseModel
from .link_tables import book_club_user, book_club_book, book_club_admin


class BookClub(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    name = AppDb.Column(AppDb.String(80), nullable=False)
    description = AppDb.Column(AppDb.String(255))

    # relationships
    posts = AppDb.relationship('Post', backref='posts', lazy='dynamic')
    users = AppDb.relationship('User', secondary=book_club_user,
                               backref=AppDb.backref('book_club',  lazy='dynamic'))
    books = AppDb.relationship('Book', secondary=book_club_book, lazy='dynamic',
                               backref=AppDb.backref('book_club', lazy=True))
    admins = AppDb.relationship('User', secondary=book_club_admin, lazy='dynamic',
                                backref=AppDb.backref('admin', lazy=True))

    def __repr__(self):
        return '<Book Club {}>'.format(self.name)
