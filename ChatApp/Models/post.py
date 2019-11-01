from datetime import datetime
from .database import BaseModel


class Post(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    title = AppDb.Column(AppDb.String(80))
    body = AppDb.Column(AppDb.String(255), nullable=False)
    user_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id'))
    book_club_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('book_club.id'))
    timestamp = AppDb.Column(AppDb.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return 'Post {0} at {1}'.format(self.body, self.timestamp)
