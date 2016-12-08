from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    mac_address = Column(String(20), nullable=False)

    def __init__(self, id=None, name=None, mac_address=None):
        self.id = id
        self.name = name
        self.mac_address = mac_address

