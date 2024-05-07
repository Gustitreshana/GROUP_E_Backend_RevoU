
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
        donatur_obj.species = donatur.species
        donatur_obj.age = donatur.age
        donatur_obj.gender = donatur.gender
        donatur_obj.special_requirement = donatur.special_requirement
        
        db.session.commit()
        return donatur_obj
    
    def delete_donatur(self, id):
        donatur_obj = Donatur.query.get(id)

        db.session.delete(donatur_obj)
        db.session.commit()
        return donatur_obj
    
    def search_donaturs(self, species):
        donaturs = Donatur.query.filter(Donatur.species.like(f"%{species}%")).all()
        return donaturs
