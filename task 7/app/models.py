from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, index=True, nullable=False)
    definition = Column(String, nullable=False)
    priority = Column(Integer, nullable=False)
    relation = Column(Integer, ForeignKey("terms.id"), nullable=True)
    author = Column(String, default="Vityaooooo")

    related_term = relationship("Term", remote_side=[id], backref="related_to")
