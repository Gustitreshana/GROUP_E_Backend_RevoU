from app.utils.db import db

donatur_donasi_association = db.Table('donatur_donasi_association',
    db.Column('donatur_id', db.Integer, db.ForeignKey('donatur.donatur_id')),
    db.Column('donasi_id', db.Integer, db.ForeignKey('donasi.donasi_id'))
)
