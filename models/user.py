from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from db import Base

class AppUser(Base):
    __tablename__ = "app_user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
