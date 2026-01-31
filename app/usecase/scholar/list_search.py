from typing import Dict, Optional
from fastapi import HTTPException
from app.domain.entities.crawler import FetchInput
from app.domain.entities.http import CookieData
from app.domain.entities.scholar.crawl_result import ScholarCrawlResult
from app.domain.port.crawler import WebCrawler
from app.domain.port.usecase import Usecase
from app.pkg.shared.headers import HEADERS
from app.pkg.utils.http_utils import create_list_cookies_data
from app.repositories.interfaces import IArticlesRepository, IScholarCookieRepository
from app.usecase.scholar.dto import (
    ScholarListSearchInputDTO,
    ScholarListSearchOutputDTO,
)


class ScholarListSearchUsecase(
    Usecase[ScholarListSearchInputDTO, ScholarListSearchOutputDTO]
):
    def __init__(
        self,
        scholar_list_crawler: WebCrawler[ScholarCrawlResult],
        scholar_cookie_repository: IScholarCookieRepository,
        articles_repository: IArticlesRepository,
    ):
        self.scholar_list_crawler = scholar_list_crawler
        self.scholar_cookie_repository = scholar_cookie_repository
        self.articles_repository = articles_repository

    async def execute(
        self, input_dto: ScholarListSearchInputDTO
    ) -> ScholarListSearchOutputDTO:
        # Construct the search URL
        search_url = f"https://scholar.google.com/scholar?q={input_dto.query}"

        cookies: Optional[Dict[str, str]] = (
            await self.scholar_cookie_repository.get_cookies()
        )
        if not cookies:
            raise HTTPException(
                status_code=500, detail={"message": "no cookies for this request"}
            )

        # Prepare fetch input
        fetch_input = FetchInput(
            url=search_url,
            method="GET",
            headers=HEADERS,
            data=None,
            cookies=create_list_cookies_data(cookies),
        )

        # Fetch and extract the scholar list
        fetch_output = await self.scholar_list_crawler.fetch_page(fetch_input)
        crawl_result = self.scholar_list_crawler.extract_page(fetch_output)

        # Save articles to the DB
        await self.articles_repository.upsert_articles(crawl_result.articles)

        # Prepare output DTO
        output_dto = ScholarListSearchOutputDTO(articles=crawl_result.articles)

        return output_dto


def new_scholar_list_search_usecase(
    scholar_list_crawler: WebCrawler[ScholarCrawlResult],
    scholar_cookie_repository: IScholarCookieRepository,
    articles_repository: IArticlesRepository,
):
    return ScholarListSearchUsecase(
        scholar_list_crawler, scholar_cookie_repository, articles_repository
    )
