from models.Base import Base
from sqlalchemy import Column, Integer, String, Float


class ComicsModel(Base):
    __tablename__ = 'comics'
    publication = Column(Integer)
    publisher = Column(String)
    title = Column(String)
    number = Column(Integer)
    vol = Column(Integer)
    year = Column(Integer)
    type = Column(String)
    condition = Column(String)
    box = Column(Integer)
    copies = Column(Integer)
