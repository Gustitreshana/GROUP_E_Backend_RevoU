from app.utils.db import db
from sqlalchemy import Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func

# Import model Donatur and Program if needed
# from app.models.donatur import Donatur
# from app.models.program import Program

class Donasi(db.Model):
    __tablename__ = "donasi"

    donasi_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donasi_datetime = db.Column(DateTime(timezone=True), server_default=func.now())
    donatur_id = db.Column(db.Integer, ForeignKey("donatur.donatur_id", ondelete="CASCADE"))
    program_id = db.Column(db.Integer, ForeignKey("program.program_id", ondelete="CASCADE"))
    pesan_doa = db.Column(db.String(255), nullable=False)
    rupiah = db.Column(DECIMAL(precision=10, scale=2))
    tipe_pembayaran = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable= False)

    # Relationship to Donatur and Program models
    donatur = db.relationship("Donatur", backref="donasi", foreign_keys=[donatur_id])
    program = db.relationship("Program", backref="donasi", foreign_keys=[program_id])
    user = db.relationship('User', backref='donasi')

    # def __init__(self, pesan_doa, rupiah, tipe_pembayaran, user, donatur, program, donasi_datetime=None):
    #     self.pesan_doa = pesan_doa
    #     self.rupiah = rupiah
    #     self.tipe_pembayaran = tipe_pembayaran
    #     self.donasi_datetime = donasi_datetime if donasi_datetime else func.now()
    #     self.user = user
    #     self.donatur = donatur
    #     self.program = program

    def __repr__(self):
        return f'<Donasi {self.donasi_id}>'
    
    def serialize(self, full=True):
        if full:
            return {
                'donasi_id': self.donasi_id,
                'user_id' : self.user_id,
                'donasi_datetime': self.donasi_datetime,
                'donatur_id': self.donatur_id,
                'program_id': self.program_id,
                'rupiah': self.rupiah,
                'tipe_pembayaran': self.tipe_pembayaran
            }
        else:
            return {
                'donasi_id': self.donasi_id,
                'user_id': self.user_id,
                'rupiah': self.rupiah,
                'tipe_pembayaran': self.tipe_pembayaran
            }

    # def __repr__(self):
    #     return f"<Donasi {self.donasi_id} from {self.donatur_id, self.program_id}>"