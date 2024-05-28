from app.models.donasi import Donasi
from app.utils.db import db

class Donasi_repo():
    def get_list_donasi(self):
        donasis = Donasi.query.all()
        return donasis

    def create_donasi(self, donasi):
        db.session.add(donasi)
        db.session.commit()
        return donasi
