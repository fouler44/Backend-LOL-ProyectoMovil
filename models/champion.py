from sqlalchemy import Column, Integer, String
from db import Base

class Champion(Base):
    __tablename__ = "champion"

    champion_id = Column(Integer, primary_key=True)
    champion_name = Column(String(20), nullable=False)
    champion_key = Column(String(25))
