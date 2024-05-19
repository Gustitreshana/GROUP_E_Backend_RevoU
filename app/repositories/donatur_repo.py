
from datetime import datetime
from app.models.donatur import Donatur
from app.utils.db import db


class Donatur_repo():
    def get_donaturs(self):
        donaturs = Donatur.query.all()
        return donaturs
    
    def create_donatur(self, donatur):
        db.session.add(donatur)
        db.session.commit()
        return donatur
    
    def update_donatur(self, id, donatur):
        donatur_obj = Donatur.query.get(id)
        donatur_obj.nama = donatur.nama
        donatur_obj.alamat = donatur.alamat
        donatur_obj.nomor_telepon = donatur.nomor_telepon
        donatur_obj.updated_at = datetime.now()
        
        db.session.commit()
        return donatur_obj
    
    def delete_donatur(self, id):
        donatur_obj = Donatur.query.get(id)

        db.session.delete(donatur_obj)
        db.session.commit()
        return donatur_obj
    
    def search_donaturs(self, nama):
        donaturs = Donatur.query.filter(Donatur.nama.like(f"%{nama}%")).all()
        return donaturs
