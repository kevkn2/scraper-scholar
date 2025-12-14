from typing import List, Optional

from fastapi import Cookie
from pydantic import BaseModel

from app.domain.entities.http import CookieData


class ScholarData(BaseModel):
    title: str
    authors: List[str]
    url: str
    year: int
    pdf_url: Optional[str] = None
    citations_url: Optional[str] = None


class ScholarCrawlResult(BaseModel):
    articles: List[ScholarData]


class ScholarCookies(BaseModel):
    GSP: CookieData
