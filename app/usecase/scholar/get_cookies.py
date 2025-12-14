from typing import Dict
from app.domain.constants import scholar
from app.domain.constants.http import METHOD_GET
from app.domain.entities.crawler import FetchInput
from app.domain.entities.scholar.crawl_result import ScholarCookies
from app.domain.port.crawler import WebCrawler
from app.domain.port.usecase import Usecase
from app.repositories.interfaces import IScholarCookieRepository
from app.usecase.scholar.dto import ScholarGetCookiesDTO


class ScholarGetCookiesUsecase(Usecase[None, ScholarGetCookiesDTO]):
    def __init__(
        self,
        scholar_main_crawler: WebCrawler[ScholarCookies],
        scholar_cookie_repository: IScholarCookieRepository,
    ):
        self.scholar_main_crawler = scholar_main_crawler
        self.scholar_cookie_repository = scholar_cookie_repository

    async def execute(self, input: None) -> ScholarGetCookiesDTO:
        fetch_input = FetchInput(url=scholar.SCHOLAR_MAIN_URL, method=METHOD_GET)

        fetch_result = await self.scholar_main_crawler.fetch_page(fetch_input)
        scholar_cookies = self.scholar_main_crawler.extract_page(fetch_result)

        await self.scholar_cookie_repository.save_cookies(scholar_cookies.model_dump())

        return ScholarGetCookiesDTO(cookies=scholar_cookies)


def new_scholar_get_cookies_usecase(
    scholar_main_crawler: WebCrawler[ScholarCookies],
    scholar_cookie_repository: IScholarCookieRepository,
):
    return ScholarGetCookiesUsecase(scholar_main_crawler, scholar_cookie_repository)
