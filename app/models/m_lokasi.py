from sqlalchemy import Column, Integer, String
from app.core.database import Base  # pastikan Base di-import dari config yang berisi declarative_base()

class MLokasi(Base):
    __tablename__ = "mlokasi"

    id_lokasi = Column(Integer, primary_key=True, autoincrement=True)
    kode_lokasi = Column(String(20), unique=True, nullable=False)
    nama_lokasi = Column(String(100), nullable=False)
    distrik = Column(Integer, nullable=True)
    tipe = Column(String(50), nullable=True)
    alamat = Column(String(200), nullable=True)
    keterangan = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<MLokasi(id_lokasi={self.id_lokasi}, nama_lokasi='{self.nama_lokasi}')>"
