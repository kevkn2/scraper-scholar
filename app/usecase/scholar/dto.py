from typing import List
from pydantic import BaseModel
from app.domain.entities.scholar.crawl_result import ScholarCookies, ScholarData


class ScholarListSearchInputDTO(BaseModel):
    query: str


class ScholarListSearchOutputDTO(BaseModel):
    articles: List[ScholarData]


class ScholarGetCookiesDTO(BaseModel):
    cookies: ScholarCookies
