from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Base class for declarative class definitions
Base = declarative_base()

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