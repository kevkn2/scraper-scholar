from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")
R = TypeVar("R")


class Usecase(ABC, Generic[T, R]):
    @abstractmethod
    def execute(self, input: T) -> R:
        pass
