from sqlalchemy import Column, String, Integer, Date, Time
from app.core.database import Base


class TTbsDalam(Base):
    __tablename__ = "TTbsDalam"

    NoTransaksi = Column(String(100), primary_key=True, index=True)
    PlatNo = Column(String(50))
    NamaDriver = Column(String(100))
    NamaProduk = Column(String(100))
    TglTransaksiOne = Column(Date)
    TimeTmbOne = Column(Time)
    TmbOne = Column(Integer)
    TglTransaksiTwo = Column(Date)
    TimeTmbTwo = Column(Time)
    TmbTwo = Column(Integer)
    NamaKebun = Column(String(50))
    Divisi = Column(String(50))
    JumlahJanjang = Column(Integer)
    Status = Column(Integer)
    NamaPT = Column(String(50))
    Total = Column(Integer)
    TotalPot = Column(Integer)
    BJR = Column(Integer)
    JenisTbs = Column(String(50))
    id_lokasi = Column(Integer, nullable=True)  # backend-only field

    def __repr__(self):
        return f"<TTbsDalam(NoTransaksi={self.NoTransaksi}, Total={self.Total}, Kebun={self.NamaKebun})>"
