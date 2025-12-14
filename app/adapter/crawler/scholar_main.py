from app.domain.entities.crawler import FetchInput, FetchOutput
from app.domain.entities.scholar.crawl_result import ScholarCookies
from app.domain.port.crawler import WebCrawler
from app.pkg.utils.http_utils import normalize_cookies
from app.pkg.utils.request_utils import async_fetch


class ScholarMainCrawler(WebCrawler[ScholarCookies]):
    async def fetch_page(self, fetch_input: FetchInput) -> FetchOutput:
        response = await async_fetch(
            url=fetch_input.url,
            method=fetch_input.method,
            headers=fetch_input.headers,
            data=fetch_input.data,
        )

        return FetchOutput(
            status_code=response.status_code,
            headers=dict(response.headers),
            data=response.text,
            cookies=normalize_cookies(response.cookies),
        )

    def extract_page(self, extract_data: FetchOutput) -> ScholarCookies:
        gsp = next(
            (c for c in extract_data.cookies if c.name == "GSP"),
            None,
        )
        return ScholarCookies(GSP=gsp)


def new_scholar_main_crawler():
    return ScholarMainCrawler()
