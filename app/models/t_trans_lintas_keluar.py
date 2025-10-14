from sqlalchemy import Column, String, Integer, Date, Time
from app.core.database import Base


class TTransLintasKeluar(Base):
    __tablename__ = "TTransLintasKeluar"

    NoTransaksi = Column(String(50), primary_key=True, index=True)
    NoDO = Column(String(50))
    NamaProduk = Column(String(50))
    TglTmb1 = Column(Date)
    TimeTmb1 = Column(Time)
    Tmb1 = Column(Integer)
    TglTmb2 = Column(Date)
    TimeTmb2 = Column(Time)
    Tmb2 = Column(Integer)
    Qty = Column(Integer)
    Terkirim = Column(Integer)
    Diterima = Column(Integer)
    Sisa = Column(Integer)
    Transportir = Column(String(50))
    PlatNo = Column(String(50))
    NamaDriver = Column(String(50))
    NoSurat = Column(String(50))
    TglSurat = Column(Date)
    Ket = Column(String(50))
    Status = Column(String(50))
    Total = Column(Integer)
    Tujuan = Column(String(50))
    NoSegel = Column(String(50))
    JumlahSegel = Column(String(50))
    Asal = Column(String(50))
    Divisi = Column(String(50))
    JumlahJjg = Column(String(50))
    BJR = Column(String(50))
    id_lokasi = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<TTransLintasKeluar(NoTransaksi={self.NoTransaksi}, Produk={self.NamaProduk}, Total={self.Total})>"
