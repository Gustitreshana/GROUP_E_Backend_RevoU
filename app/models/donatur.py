from app.utils.db import db
from sqlalchemy import Integer, String, Text, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func


class Donatur(db.Model):
    __tablename__ = 'donatur'

    donatur_id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(200), nullable=False)
    alamat = db.Column(db.String(100), nullable=False)
    nomor_telepon = db.Column(db.String(255), nullable= False, unique=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now())
    

    # Relasi dengan model User
    # user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="donatur")

    def __repr__(self):
        return f'<Donatur {self.donatur_id}>'
    
    def serialize(self, full=True):
        if full:
            return {
                'id': self.donatur_id,
                'nama': self.nama,
                'alamat': self.alamat,
                'user_id': self.user_id,
                'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                'id': self.donatur_id,
                'nama': self.nama,
                'alamat': self.alamat,
                'user_id': self.user_id
            }