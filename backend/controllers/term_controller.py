from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from models import PlatformEnum, SearchTerm
from database import get_db

class TermBase(BaseModel):
    term: str
    platform: PlatformEnum

class TermCreate(TermBase):
    pass

class TermUpdate(TermBase):
    pass

# CRUD operations for search terms
def create_term(term: TermCreate, db: Session = Depends(get_db)):
    try:
        term.platform = term.platform.value
        db_term = SearchTerm(**term.model_dump())
        db.add(db_term)
        db.commit()
        db.refresh(db_term)
        return db_term
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def list_term(db: Session = Depends(get_db)):
    try:
        terms = db.query(SearchTerm).options(joinedload(SearchTerm.results)).all()
        return terms
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_term(term_id: int, db: Session = Depends(get_db)):
    try:
        term = db.query(SearchTerm).options(joinedload(SearchTerm.results)).filter(SearchTerm.id == term_id).first()
        if term is None:
            raise HTTPException(status_code=404, detail="Search term not found")
        return term
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_term(term_id: int, term: TermUpdate, db: Session = Depends(get_db)):
    try:
        if term.platform:
            term.platform = term.platform.value

        db_term = db.query(SearchTerm).filter(SearchTerm.id == term_id).first()
        if db_term is None:
            raise HTTPException(status_code=404, detail="Search term not found")
        for key, value in term.model_dump().items():
            setattr(db_term, key, value)
        db.commit()
        db.refresh(db_term)
        return db_term
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_term(term_id: int, db: Session = Depends(get_db)):
    try:
        db_term = db.query(SearchTerm).filter(SearchTerm.id == term_id).first()
        if db_term is None:
            raise HTTPException(status_code=404, detail="Search term not found")
        db.delete(db_term)
        db.commit()
        return {"message": "Search term deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))