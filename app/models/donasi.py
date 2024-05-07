

from app.utils.db import db
from sqlalchemy import Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import func
from app.models.donatur import Donatur

class Donasi(db.Model):
    __tablename__ = "donasi"

    donasi_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donasi_datetime = db.Column(DateTime(timezone=True), server_default=func.now())
    donatur_id = db.Column(db.Integer, ForeignKey("donatur.donatur_id", ondelete="CASCADE"))
    program_id = db.Column(db.Integer, ForeignKey("program.program_id", ondelete="CASCADE"))
    pesan_doa = db.Column(db.String(255), nullable= False)
    rupiah = db.Column(DECIMAL(precision=10, scale=2))
    tipe_pembayaran = db.Column(db.String(255), nullable= False)

    # # Relationship to Account model for the 'from_account'
    # from_account = relationship("Account", foreign_keys=[from_account_id])

    # # Relationship to Account model for the 'to_account'
    # to_account = relationship("Account", foreign_keys=[to_account_id])

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