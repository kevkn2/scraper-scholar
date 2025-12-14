from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.domain.entities.crawler import FetchInput, FetchOutput

T = TypeVar("T")


class WebCrawler(ABC, Generic[T]):
    @abstractmethod
    def fetch_page(self, fetch_input: FetchInput) -> FetchOutput:
        pass

    @abstractmethod
    def extract_page(self, extract_data: FetchOutput) -> T:
        pass
