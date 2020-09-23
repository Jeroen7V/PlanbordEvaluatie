from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.types import DateTime
from .database import Base


class Result(Base):
    __tablename__ = "Results"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    symbol = Column(String(255), index=True)
    task = Column(String(255), index=True)
    difficult = Column(Boolean)
    like = Column(Boolean)