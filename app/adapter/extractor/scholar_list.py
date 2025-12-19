import re
from typing import List, Optional, Tuple
from bs4 import Tag
from app.domain.entities.scholar.crawl_result import ScholarData
from app.domain.port.extractor import Extractor
from app.pkg.utils.bs4_utils import extract_link, extract_text, find_div


class ScholarListExtractor(Extractor[Optional[ScholarData]]):
    def extract(self, content: Tag) -> Optional[ScholarData]:
        # Find the main content area
        ri_div = find_div(content, "gs_ri")
        if not ri_div:
            return None

        articles = ScholarData(
            title="",
            authors=[],
            url="",
            year=0,
        )

        # Extract title and link
        title_tag = ri_div.find("h3", class_="gs_rt")
        if title_tag:
            articles.title, articles.url = self._extract_title_and_link(title_tag)

        # Extract PDF/HTML link
        ggs_div = find_div(content, "gs_ggs")
        if ggs_div:
            articles.pdf_url = self._extract_pdf_url(ggs_div)

        # Extract authors and publication info
        author_div = find_div(ri_div, "gs_a")
        if author_div:
            articles.year, articles.authors = self._extract_year_and_authors(author_div)

        # Extract citation count and related links
        footer_div = find_div(ri_div, "gs_fl")
        if footer_div:
            articles.citations_url = self._extract_citation_url(footer_div)

        return articles

    def _extract_title_and_link(self, title_tag: Tag) -> Tuple[str, str]:
        link_tag = title_tag.find("a")
        text = extract_text(link_tag) or extract_text(title_tag)
        url = extract_link(link_tag)

        return text, url

    def _extract_pdf_url(self, ggs_div: Tag) -> str:
        pdf_link = ggs_div.find("a")
        return extract_link(pdf_link)

    def _extract_year_and_authors(self, author_div: Tag) -> Tuple[int, List[str]]:
        authors_and_publication = extract_text(author_div)
        year = re.match(r".*\,\s(\d+).*", authors_and_publication)
        year_int = int(year.group(1)) if year else 0
        authors = [extract_text(a) for a in author_div.find_all("a")]

        return year_int, authors

    def _extract_citation_url(self, footer_div: Tag) -> str:
        for link in footer_div.find_all("a"):
            link_text = extract_text(link)
            if any(keyword in link_text for keyword in ["Dirujuk", "Cited by"]):
                return extract_link(link)


def new_scholar_list_extractor():
    return ScholarListExtractor()
