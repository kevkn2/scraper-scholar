from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bs4 import Tag

T = TypeVar("T")


class Extractor(ABC, Generic[T]):
    @abstractmethod
    def extract(self, content: Tag) -> T:
        pass
