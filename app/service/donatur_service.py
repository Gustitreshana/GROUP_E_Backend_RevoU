
from datetime import datetime
from app.repositories.donatur_repo import Donatur_repo
from app.models.donatur import Donatur

    
class Donatur_service:
    def __init__(self):
        self.donatur_repo = Donatur_repo()

    def get_donaturs(self):
        donaturs = self.donatur_repo.get_donaturs()
        return [donatur.serialize() for donatur in donaturs]

    def search_donaturs(self, species):
        donaturs = self.donatur_repo.search_donaturs(species)
        return [donatur.serialize() for donatur in donaturs]

    def create_donatur(self, donatur_data_dto):
        donatur = Donatur()

        donatur.nama = donatur_data_dto.nama
        donatur.alamat = donatur_data_dto.alamat
        donatur.nomor_telepon = donatur_data_dto.nomor_telepon
        donatur.created_at = datetime.now()
        donatur.updated_at = datetime.now()

        created_donatur = self.donatur_repo.create_donatur(donatur)
        return created_donatur.serialize()

    # cara ke-1 tanpa DTO
    # def update_donatur(self, id, donatur_data):
    #     updated_donatur = self.donatur_repo.update_donatur(id, donatur_data)
    #     return updated_donatur
    
    def update_donatur(self, id, donatur_data_dto):
        updated_donatur = self.donatur_repo.update_donatur(id, donatur_data_dto)
        return updated_donatur.serialize()
    
    def delete_donatur(self, id):
        donatur = Donatur.query.get(id)
        if not donatur:
            return "Donatur not available"
        
        delete_donatur = self.donatur_repo.delete_donatur(id)
        return delete_donatur.serialize()