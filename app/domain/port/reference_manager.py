from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class ReferenceManager(ABC, Generic[T]):
    @abstractmethod
    def get_documents(self, access_token: str) -> List[T]:
        pass
