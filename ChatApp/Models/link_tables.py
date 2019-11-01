from .database import BaseModel

AppDb = BaseModel.db

# BOOK CLUB USERS

book_club_user = AppDb.Table(
    'book_club_user',
    AppDb.Column('book_club_id', AppDb.Integer, AppDb.ForeignKey('book_club.id'), primary_key=True),
    AppDb.Column('user_id', AppDb.Integer, AppDb.ForeignKey('users.id'), primary_key=True)
)

# BOOK CLUB BOOKS

book_club_book = AppDb.Table(
    'book_club_book',
    AppDb.Column('book_club_id', AppDb.Integer, AppDb.ForeignKey('book_club.id'), primary_key=True),
    AppDb.Column('book_id', AppDb.Integer, AppDb.ForeignKey('book.id'), primary_key=True)
)

# ADMINS

book_club_admin = AppDb.Table(
    'admins',
    AppDb.Column('book_club_id', AppDb.Integer, AppDb.ForeignKey('book_club.id'), primary_key=True),
    AppDb.Column('user_id', AppDb.Integer, AppDb.ForeignKey('users.id'), primary_key=True)
)

# FOLLOWERS

followers = AppDb.Table(
    'followers',
    AppDb.Column('follower_id', AppDb.Integer, AppDb.ForeignKey('users.id')),
    AppDb.Column('followed_id', AppDb.Integer, AppDb.ForeignKey('users.id'))
)
