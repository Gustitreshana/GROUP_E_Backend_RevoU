from utils.db import db
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    realname = db.Column(db.String(100))
    address = db.Column(db.String(200))
    occupation = db.Column(db.String(100))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'realname': self.realname,
            'address': self.address,
            'occupation': self.occupation,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
    def __repr__(self):
        return f"<User {self.id}>"