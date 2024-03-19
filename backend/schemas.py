from pydantic import BaseModel

class TermBase(BaseModel):
    term: str
    platform: str

class TermCreate(TermBase):
    pass

class TermUpdate(TermBase):
    pass