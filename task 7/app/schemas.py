from pydantic import BaseModel
from typing import Optional

class TermBase(BaseModel):
    term: str
    definition: str
    priority: int
    relation: Optional[int] = None
    author: Optional[str] = "Vityaooooo"

class TermCreate(TermBase):
    pass

class TermUpdate(TermBase):
    pass

class TermResponse(TermBase):
    id: int

    class Config:
        orm_mode = True
