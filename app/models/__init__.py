# from app.models.donatur import Donatur
# from app.models.donasi import Donasi
# from app.models.association import donatur_donasi_association
# from sqlalchemy.orm import relationship

# # Tambahkan relasi setelah kedua kelas terdefinisi
# Donatur.donasi = relationship("Donasi", secondary=donatur_donasi_association, back_populates="donatur_donasi")
# Donasi.donatur_donasi = relationship("Donatur", secondary=donatur_donasi_association, back_populates="donasi")
