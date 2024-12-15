from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, Base, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/terms", response_model=list[schemas.TermResponse])
async def get_terms(db: Session = Depends(get_db)):
    return db.query(models.Term).all()

@app.get("/terms/{term_id}", response_model=schemas.TermResponse)
async def get_term(term_id: int, db: Session = Depends(get_db)):
    term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term

@app.post("/terms", response_model=schemas.TermResponse)
async def create_term(term: schemas.TermCreate, db: Session = Depends(get_db)):
    new_term = models.Term(**term.dict())
    db.add(new_term)
    db.commit()
    db.refresh(new_term)
    return new_term

@app.put("/terms/{term_id}", response_model=schemas.TermResponse)
async def update_term(term_id: int, updated_term: schemas.TermUpdate, db: Session = Depends(get_db)):
    term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    for key, value in updated_term.dict(exclude_unset=True).items():
        setattr(term, key, value)
    db.commit()
    db.refresh(term)
    return term

@app.delete("/terms/{term_id}")
async def delete_term(term_id: int, db: Session = Depends(get_db)):
    term = db.query(models.Term).filter(models.Term.id == term_id).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    db.delete(term)
    db.commit()
    return {"message": f"Term with ID {term_id} deleted successfully"}
