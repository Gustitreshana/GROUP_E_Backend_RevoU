from utils.db import db
from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.sql import func
from sqlalchemy import DateTime

class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(Integer, primary_key=True)
    nominal = db.Column(Float, nullable=False)
    from_id = db.Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to User
    donor = db.relationship('User', backref='donations', foreign_keys=[from_id])

    def to_dict(self):
        return {
            'id': self.id,
            'nominal': self.nominal,
            'from_id': self.from_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f"<Donation {self.id} from {self.from_id}>"
