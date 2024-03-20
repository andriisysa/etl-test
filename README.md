## Pre-requirements
Go to https://newsapi.org/account and get api_key by creating an account


## Setup env
### Setup postgresql env
There is postgresql env example in postgresql directory.
You can specify postgres username and password there. \
Note: You must add .env file in the postgresql directory.

example:

```bash
POSTGRES_USER=admin
POSTGRES_PASSWORD=pass
```

### Setup backend env
There is backend env example in backend directory.
You can specify postgres username and password. \

example:

```bash
DATABASE_URL=postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost/postgres
NEWS_API_KEY=<YOUR_NEWS_API_KEY>
```

## Run server
Run following command

```bash
docker compose up
```

## Backend
Backend is using fastapi, Sqlalchemy ORM and alembic (for db migration). \
Fastapi serves backend endpoints for managing serach terms. \
There is 1 scheduler to run search job every 1 day and get news data through Newapi and fill db table.

## Models
There are 2 models SearchTerm and SearchResult

SearchTerm has term/query for searching social medial/news and will be handled by fastapi endpoints.

SearchResult contains searched results from social media/news api with the search term. (it will be filled by scheduler job)

```bash
class SearchTerm(Base):
    __tablename__ = "search_terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, index=True)
    platform = Column(String, nullable=False)
    # unix timestamp
    last_searched = Column(Integer, nullable=True)

    # Define relationship with SearchResult
    results = relationship("SearchResult", back_populates="term")

class SearchResult(Base):
    __tablename__ = "search_results"

    id = Column(Integer, primary_key=True, index=True)
    term_id = Column(Integer, ForeignKey("search_terms.id"))
    term = relationship("SearchTerm", back_populates="results")
    result_id = Column(String, unique=True, index=True)
    result_data = Column(JSON)
    # unix timestamp
    searched_at = Column(Integer)
```