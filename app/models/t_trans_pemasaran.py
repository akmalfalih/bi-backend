from sqlalchemy import Column, String, Integer, Date, Time, Text
from app.core.database import Base

class TTransPemasaran(Base):
    __tablename__ = "TTransPemasaran"

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
    TujuanPT = Column(String(50))
    TujuanKebun = Column(String(50))
    NamaPT = Column(String(50))
    Status = Column(Integer)
    NamaUser = Column(String(50))
    Total = Column(Integer)
    TotalPot = Column(Integer)
    BJR = Column(Integer)
    JenisTbs = Column(String(50))
