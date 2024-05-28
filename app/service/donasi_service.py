from datetime import datetime
from app.models.donatur import Donatur
from app.models.program import Program
from app.repositories.donasi_repo import Donasi_repo
from app.models.donasi import Donasi
from app.models.user import User

class Donasi_service:
    def __init__(self):
        self.donasi_repo = Donasi_repo()

    def create_donasi(self, donasi_data_dto, user_id, donatur_id, program_id):
        # Mengambil objek User berdasarkan user_id
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"Tidak dapat menemukan user dengan ID {user_id}")

        donatur = Donatur.query.get(donatur_id)
        if not user:
            raise ValueError(f"Tidak dapat menemukan donatur dengan ID {donatur_id}")

        program = Program.query.get(program_id)
        if not user:
            raise ValueError(f"Tidak dapat menemukan program dengan ID {program_id}")

        # Membuat objek Program dengan data yang diberikan
        donasi = Donasi()

        donasi.pesan_doa=donasi_data_dto.pesan_doa
        donasi.rupiah=donasi_data_dto.rupiah
        donasi.tipe_pembayaran=donasi_data_dto.tipe_pembayaran
        donasi.user = user  # Mengatur objek User
        donasi.donatur=donatur
        donasi.program=program
        donasi.donasi_datetime=datetime.now()
        

        # Menyimpan donasi baru ke database
        created_donasi = self.donasi_repo.create_donasi(donasi)
        return created_donasi.serialize()






    
    # def get_donasis(self, user_id):
    #     # Mengambil objek User berdasarkan user_id
    #     user = User.query.get(user_id)
    #     if not user:
    #         raise ValueError(f"Tidak dapat menemukan user dengan ID {user_id}")
        
    #     donasis = self.donasi_repo.get_list_donasi()
    #     return [donasi.serialize() for donasi in donasis]