import sys
import signal
from threading import Thread
import uvicorn

from fastapi import FastAPI
from database import engine
from models import Base
from routers.term import term_router

from scheduler import run_scheduler, stop_scheduler

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"Hello": "World"}

app.include_router(term_router, prefix="/terms")

def signal_handler(sig, frame):
    print('Ctrl+C detected, stopping scheduler...')
    stop_scheduler()
    sys.exit(0)

if __name__ == "__main__":
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8000)

    signal.signal(signal.SIGINT, signal_handler)
