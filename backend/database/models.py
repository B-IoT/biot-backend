from sqlalchemy import Column, Integer, Float, String

from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    status = Column(String, index=True)
    battery = Column(Integer)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)