from typing import List
from bs4 import BeautifulSoup
from app.domain.entities.crawler import FetchInput, FetchOutput
from app.domain.entities.scholar.crawl_result import ScholarCrawlResult, ScholarData
from app.domain.port.crawler import WebCrawler
from app.domain.port.extractor import Extractor
from app.pkg.utils.http_utils import get_to_httpx_cookies
from app.pkg.utils.request_utils import async_fetch


class ScholarListCrawler(WebCrawler[ScholarCrawlResult]):
    def __init__(self, extractor: Extractor[ScholarCrawlResult]):
        self.extractor = extractor

    async def fetch_page(self, fetch_input: FetchInput) -> FetchOutput:
        response = await async_fetch(
            url=fetch_input.url,
            method=fetch_input.method,
            headers=fetch_input.headers,
            data=fetch_input.data,
            cookies=get_to_httpx_cookies(fetch_input.cookies),
        )

        return FetchOutput(
            status_code=response.status_code,
            headers=dict(response.headers),
            data=response.text,
        )

    def extract_page(self, extract_data: FetchOutput) -> ScholarCrawlResult:
        soup = BeautifulSoup(extract_data.data, "html.parser")

        articles: List[ScholarData] = []

        article_divs = soup.find_all("div", class_="gs_r gs_or gs_scl")
        for article_div in article_divs:
            article_data = self.extractor.extract(article_div)
            if article_data:
                articles.append(article_data)

        return ScholarCrawlResult(articles=articles)


def new_scholar_list_crawler(extractor: Extractor[ScholarCrawlResult]):
    return ScholarListCrawler(extractor=extractor)
