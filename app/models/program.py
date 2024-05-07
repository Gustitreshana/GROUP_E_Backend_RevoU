from app.utils.db import db
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import func
# from app.models.review import Review

class Program(db.Model):
    __tablename__ = "program"
    program_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_program = db.Column(db.String(200), nullable=False)
    lokasi_program = db.Column(db.String(100), nullable=False)
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship list
    # reviews = relationship("Review", cascade="all,delete-orphan")
    def as_dict(self):
        return {
            'program_id': self.program_id,
            'nama_program': self.nama_program,
            'lokasi_program': self.lokasi_program,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<Program {self.program_id}>'