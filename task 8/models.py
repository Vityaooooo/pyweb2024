from sqlalchemy import Column, Integer, String
from database import Base

class Term(Base):
    __tablename__ = "terms"
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, index=True)
    definition = Column(String)
    priority = Column(Integer, default=0)
    relation = Column(Integer, default=0)
    author = Column(String, default="Vityaooooo")