from app.utils.db import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Program(db.Model):
    __tablename__ = "program"
    
    program_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    nama_program = db.Column(db.String(200), nullable=False)
    lokasi_program = db.Column(db.String(100), nullable=False)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())

    user = db.relationship("User", back_populates="programs")
    
    def __repr__(self):
        return f'<Program {self.program_id}>'

    # def as_dict(self):
    #     return {
    #         'program_id': self.program_id,
    #         'user_id': self.user_id,
    #         'nama_program': self.nama_program,
    #         'lokasi_program': self.lokasi_program,
    #         'created_at': self.created_at,
    #         'updated_at': self.updated_at
    #     }

    def serialize(self, full=True):
        if full:
            return {
                'program_id': self.program_id,
                'user_id': self.user_id,
                'nama_program': self.nama_program,
                'lokasi_program': self.lokasi_program,
                'created_at': self.created_at,
                'updated_at': self.updated_at
            }
        else:
            return {
                'program_id': self.program_id,
                'user_id': self.user_id,
                'nama_program': self.nama_program,
                'lokasi_program': self.lokasi_program
            }

