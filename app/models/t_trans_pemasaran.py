from sqlalchemy import Column, String, Integer, Date, Time
from app.core.database import Base


class TTransPemasaran(Base):
    __tablename__ = "TTransPemasaran"

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
    BeratTarra = Column(Integer)
    KadarKotoran = Column(String(50))
    KadarAir = Column(String(50))
    Moisture = Column(String(50))
    FFA = Column(String(50))
    IV = Column(String(50))
    Suhu = Column(Integer)
    NoTangki = Column(String(50))
    NoSegel = Column(String(50))
    JmlSegel = Column(String(50))
    NoBlangko = Column(String(50))
    Pemeriksa = Column(String(50))
    Status = Column(Integer)
    Asal = Column(String(50))
    Tujuan = Column(String(50))
    NoRef = Column(String(50))
    TotalTmb = Column(Integer)
    StatusSambungDO = Column(String(50))
    NoSambungDO = Column(String(50))
    id_lokasi = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<TTransPemasaran(NoTransaksi={self.NoTransaksi}, Produk={self.NamaProduk}, TotalTmb={self.TotalTmb})>"
