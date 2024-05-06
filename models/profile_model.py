from utils.db import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    realname = db.Column(db.String(100))
    address = db.Column(db.String(200))
    occupation = db.Column(db.String(100))
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'realname': self.realname,
            'address': self.address,
            'occupation': self.occupation,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f"<Profile {self.id} for user {self.user_id}>"
