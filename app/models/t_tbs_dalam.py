from sqlalchemy import Column, String, Integer, Date, Time, Text
from app.core.database import Base

class TTbsDalam(Base):
    __tablename__ = "TTbsDalam"

    NoTransaksi = Column(Text, primary_key=True)
    PlatNo = Column(String(50))
    NamaDriver = Column(Text)
    NamaProduk = Column(Text)
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
