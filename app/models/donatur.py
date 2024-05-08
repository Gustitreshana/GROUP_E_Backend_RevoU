from app.utils.db import db
from sqlalchemy import Integer, String, Text, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

donatur_donasi_association = db.Table('donatur_donasi_association',
    db.Column('donatur_id', db.Integer, db.ForeignKey('donatur.donatur_id')),
    db.Column('donasi_id', db.Integer, db.ForeignKey('donasi.donasi_id'))
)

class Donatur(db.Model):
    __tablename__ = 'donatur'

    donatur_id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(200), nullable=False)
    alamat = db.Column(db.String(100), nullable=False)
    nomor_telepon = db.Column(db.String(255), nullable= False, unique=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="donatur")
    donasi = relationship("Donasi", secondary=donatur_donasi_association, back_populates="donatur_donasi")

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
