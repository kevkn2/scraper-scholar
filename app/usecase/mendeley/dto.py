from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class RedirectInputDTO(BaseModel):
    code: str
    state: str


class RedirectOutputDTO(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class ListDocumentsInputDTO(BaseModel):
    page: int


class ListDocumentsOutputDTO(BaseModel, Generic[T]):
    documents: list[T]
