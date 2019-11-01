import ChatApp
from ChatApp.Models.database import BaseModel
from ChatApp import login

from .link_tables import followers

from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5

from flask_login import UserMixin


class User (UserMixin, BaseModel.db.Model):
    AppDb = BaseModel.db
    __tablename__ = 'users'
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    first_name = AppDb.Column(AppDb.String(35), nullable=False)
    last_name = AppDb.Column(AppDb.String(35), nullable=False)
    username = AppDb.Column(AppDb.String(35), nullable=False, unique=True, index=True)
    email = AppDb.Column(AppDb.String(80), nullable=False, index=True)
    password = AppDb.Column(AppDb.String(255), nullable=False)

    #  relationships
    posts = AppDb.relationship('Post', backref='author', lazy='dynamic')
    followed = AppDb.relationship(
        'User',
        secondary=followers,
        primaryjoin=followers.c.follower_id == id,
        secondaryjoin=followers.c.followed_id == id,
        backref=AppDb.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(pwhash=self.password, password=password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


