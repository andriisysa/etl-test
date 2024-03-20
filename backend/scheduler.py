
import os
import schedule
import time

from sqlalchemy.orm import Session
from database import get_db
from models import SearchTerm, SearchResult
from newsapi import NewsApiClient

from dotenv import load_dotenv

load_dotenv()

scheduleEnabled = False

newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

def search_news():
    all_articles = newsapi.get_everything(q='bitcoin', from_param='2024-03-01')
    print(all_articles)
    for article in all_articles.get('articles'):
        print(article)

def run_scheduler():
    def search(db: Session):
        print("I'm working...")

        terms = db.query(SearchTerm).all()
        print(terms)
        for term in terms:
            print(term)
            pass

    schedule.every().minutes.do(search, db=next(get_db()))

    global scheduleEnabled
    while scheduleEnabled:
        schedule.run_pending()
        time.sleep(60)

def stop_scheduler():
    global scheduleEnabled
    scheduleEnabled = False
