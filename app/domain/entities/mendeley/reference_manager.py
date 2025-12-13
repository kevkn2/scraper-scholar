from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Author(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Identifiers(BaseModel):
    doi: Optional[str] = None
    isbn: Optional[str] = None
    issn: Optional[str] = None
    pmid: Optional[str] = None
    arxiv: Optional[str] = None


class MendeleyDocument(BaseModel):
    id: str
    type: Optional[str] = None  # journal, book, etc.
    title: Optional[str] = None
    abstract: Optional[str] = None
    year: Optional[int] = None

    authors: List[Author] = Field(default_factory=list)

    source: Optional[str] = None  # journal or conference name
    identifiers: Optional[Identifiers] = None

    created: Optional[datetime] = None
    last_modified: Optional[datetime] = None

    class Config:
        extra = "ignore"  # VERY IMPORTANT
