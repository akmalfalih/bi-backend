from sqlalchemy import Column, String, Integer, Date, Time
from app.core.database import Base


class TTransLintas(Base):
    __tablename__ = "TTransLintas"

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
    Status = Column(Integer)
    Total = Column(Integer)
    Tujuan = Column(String(50))
    id_lokasi = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<TTransLintas(NoTransaksi={self.NoTransaksi}, Produk={self.NamaProduk}, Total={self.Total})>"
