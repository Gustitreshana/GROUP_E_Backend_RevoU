from app.utils.db import db
from sqlalchemy import Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
from app.models.donatur import Donatur

donatur_donasi_association = db.Table('donatur_donasi_association',
    db.Column('donatur_id', db.Integer, db.ForeignKey('donatur.donatur_id')),
    db.Column('donasi_id', db.Integer, db.ForeignKey('donasi.donasi_id'))
)

class Donasi(db.Model):
    __tablename__ = "donasi"

    donasi_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donasi_datetime = db.Column(DateTime(timezone=True), server_default=func.now())
    donatur_id = db.Column(db.Integer, ForeignKey("donatur.donatur_id", ondelete="CASCADE"))
    program_id = db.Column(db.Integer, ForeignKey("program.program_id", ondelete="CASCADE"))
    pesan_doa = db.Column(db.String(255), nullable= False)
    rupiah = db.Column(DECIMAL(precision=10, scale=2))
    tipe_pembayaran = db.Column(db.String(255), nullable= False)

    donatur = relationship("Donatur", secondary=donatur_donasi_association, back_populates="donasi")

    def __repr__(self):
        return f'<Donasi {self.donasi_id}>'
    
    def serialize(self, full=True):
        if full:
            return {
                'donasi_id': self.donasi_id,
                'donasi_datetime': self.donasi_datetime,
                'donatur_id': self.donatur_id,
                'program_id': self.program_id,
                'rupiah': self.rupiah,
                'tipe_pembayaran': self.tipe_pembayaran
            }
        else:
            return {
                'donasi_id': self.donasi_id,
                'donatur_id': self.donatur_id,
                'rupiah': self.rupiah,
                'tipe_pembayaran': self.tipe_pembayaran
            }
