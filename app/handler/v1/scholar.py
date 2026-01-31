from typing import Annotated, Dict
from fastapi import APIRouter
from fastapi.params import Depends

from app.adapter.crawler.scholar_list import new_scholar_list_crawler
from app.adapter.crawler.scholar_main import new_scholar_main_crawler
from app.adapter.extractor.scholar_list import new_scholar_list_extractor
from app.database.db_session import get_db_session
from app.domain.port.usecase import Usecase
from app.repositories.adapter.articles_repository import new_articles_repository
from app.repositories.adapter.scholar_cookie_repository import (
    new_scholar_cookie_repository,
)
from app.usecase.scholar.dto import (
    ScholarListSearchInputDTO,
    ScholarListSearchOutputDTO,
)
from app.usecase.scholar.get_cookies import new_scholar_get_cookies_usecase
from app.usecase.scholar.list_search import new_scholar_list_search_usecase


v1_scholar_router = APIRouter()


def get_scholar_get_cookies_usecase():
    scholar_cookie_repository = new_scholar_cookie_repository()
    scholar_main_crawler = new_scholar_main_crawler()
    scholar_get_cookies_usecase = new_scholar_get_cookies_usecase(
        scholar_main_crawler=scholar_main_crawler,
        scholar_cookie_repository=scholar_cookie_repository,
    )

    return scholar_get_cookies_usecase


def get_scholar_list_search_usecase(session=Depends(get_db_session)):
    scholar_cookie_repository = new_scholar_cookie_repository()
    scholar_list_crawler = new_scholar_list_crawler(
        extractor=new_scholar_list_extractor()
    )
    articles_repository = new_articles_repository(session=session)

    scholar_list_search_usecase = new_scholar_list_search_usecase(
        scholar_cookie_repository=scholar_cookie_repository,
        scholar_list_crawler=scholar_list_crawler,
        articles_repository=articles_repository,
    )

    return scholar_list_search_usecase


@v1_scholar_router.get("/cookies")
async def scholar_get_cookies(
    usecase: Annotated[
        Usecase[None, Dict[str, str]], Depends(get_scholar_get_cookies_usecase)
    ],
):
    cookies = await usecase.execute(None)
    return cookies


@v1_scholar_router.get("/list-search")
async def scholar_list_search(
    query: str,
    usecase: Annotated[
        Usecase[ScholarListSearchInputDTO, ScholarListSearchOutputDTO],
        Depends(get_scholar_list_search_usecase),
    ],
):
    input_dto = ScholarListSearchInputDTO(query=query)
    output_dto = await usecase.execute(input_dto)

    return output_dto
