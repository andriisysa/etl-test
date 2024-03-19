import os
import sys
import asyncio
import signal
from threading import Thread
import schedule
import time

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, SearchTerm, SearchResult
from schemas import TermCreate, TermUpdate
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"Hello": "World"}

# CRUD operations for search terms
@app.post("/terms/")
def create_term(term: TermCreate, db: Session = Depends(get_db)):
    term = SearchTerm(**term.model_dump())
    db.add(term)
    db.commit()
    db.refresh(term)
    return term

@app.get("/terms/{term_id}")
def get_term(term_id: int, db: Session = Depends(get_db)):
    term = db.query(SearchTerm).filter(SearchTerm.id == term_id).first()
    if term is None:
        raise HTTPException(status_code=404, detail="Search term not found")
    return term

@app.put("/terms/{term_id}")
def update_term(term_id: int, term: TermUpdate, db: Session = Depends(get_db)):
    term = db.query(SearchTerm).filter(SearchTerm.id == term_id).first()
    if term is None:
        raise HTTPException(status_code=404, detail="Search term not found")
    for key, value in term.model_dump().items():
        setattr(term, key, value)
    db.commit()
    db.refresh(term)
    return term

@app.delete("/terms/{term_id}")
def delete_term(term_id: int, db: Session = Depends(get_db)):
    term = db.query(SearchTerm).filter(SearchTerm.id == term_id).first()
    if term is None:
        raise HTTPException(status_code=404, detail="Search term not found")
    db.delete(term)
    db.commit()
    return {"message": "Search term deleted successfully"}

scheduleEnabled = False

def run_scheduler():
    def job(db: Session):
        print("I'm working...")

        terms = db.query(SearchTerm).all()
        print(terms)
        for term in terms:
            print(term)
            pass

    schedule.every().minutes.do(job, db=next(get_db()))

    global scheduleEnabled
    while scheduleEnabled:
        schedule.run_pending()
        time.sleep(60)

def signal_handler(sig, frame):
    global scheduleEnabled
    print('Ctrl+C detected, stopping scheduler...')
    scheduleEnabled = False
    sys.exit(0)

if __name__ == "__main__":
    scheduleEnabled = True

    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8000)

    signal.signal(signal.SIGINT, signal_handler)
