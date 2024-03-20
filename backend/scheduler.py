import os
import schedule
import time
import json
import hashlib

from sqlalchemy.orm import Session
from database import get_db
from models import PlatformEnum, SearchTerm, SearchResult
from newsapi import NewsApiClient
from utils.time import get_now_unix, unix_to_date_string

from dotenv import load_dotenv

load_dotenv()

schedule_enabled = False
is_running = False

newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

def search_news(db: Session, term: SearchTerm):
    try:
        if term.last_searched:
            date_str = unix_to_date_string(term.last_searched, '%Y-%m-%dT%H:%M:%S')
            all_articles = newsapi.get_everything(q=term.term, from_param=date_str)
            pass
        else:
            all_articles = newsapi.get_everything(q=term.term)

        print(term.term, ":", len(all_articles.get('articles')))

        for article in all_articles.get('articles'):
            try:
                db_result = SearchResult()
                db_result.term_id = term.id
                db_result.term = term
                db_result.result_data = article
                
                result_str = json.dumps(article, sort_keys=True)
                db_result.result_id = hashlib.sha256(result_str.encode()).hexdigest()
                db_result.searched_at = get_now_unix()
                db.add(db_result)
                db.commit()
            except Exception as e:
                # If adding the article fails (e.g., due to duplicate result_id),
                # rollback the transaction and handle the exception
                db.rollback()
                print(f"Error occurred while searching news for term '{term.term}': {str(e)}")

        term.last_searched = get_now_unix()
        db.commit()
    except Exception as e:
        print(f"Error occurred while searching news for term '{term.term}': {str(e)}")

def search_terms(db: Session):
    global is_running
    if is_running:
        print('search is running..., should be returned')
        return
    
    is_running = True
    print("scheduler starts...")

    # Calculate the datetime 24 hours ago
    twenty_four_hours_ago = get_now_unix() - (24 * 60 * 60)

    # Query for SearchTerm objects where last_searched is either NULL or before 24 hours ago
    terms = db.query(SearchTerm).filter(
        (SearchTerm.last_searched.is_(None)) |
        (SearchTerm.last_searched < twenty_four_hours_ago)
    ).all()
    print('terms', ":", len(terms))

    for term in terms:
        if term.platform == PlatformEnum.NewsApi.value:
            search_news(db, term)

    is_running = False
    print("scheduler ends...")

def run_scheduler():
    schedule.every().day.at("00:00").do(search_terms, db=next(get_db()))

    global schedule_enabled
    schedule_enabled = True

    while schedule_enabled:
        schedule.run_pending()
        time.sleep(60)

def stop_scheduler():
    global schedule_enabled
    schedule_enabled = False
