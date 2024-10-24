from sqlalchemy import Column, Integer, String, Numeric, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base
from fetcher.utils import pg_db


Base = declarative_base()

class ARPValue(Base):
    __tablename__ = pg_db

    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange_name = Column(String)
    token = Column(String)
    arp_value = Column(Numeric, nullable=False)
    timestamp = Column(DateTime, default=datetime)
