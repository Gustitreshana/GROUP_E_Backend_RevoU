from app.utils.db import db
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import bcrypt

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(191), nullable=False, unique= True)
    name = db.Column(db.String(191), nullable=False)
    password = db.Column(db.String(191), nullable=False)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    role = db.Column(db.String(100), nullable=True)
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relasi dengan model Program
    programs = db.relationship("Program", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.id}>'

    def serialize(self, full=True):
        if full:
            return {
                'id': self.id,
                'email': self.email,
                'name': self.name,
                'password': self.password,
                'role': self.role,
                'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                'id': self.id,
                'email': self.email,
                'name': self.name,
                'role': self.role
            }
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
