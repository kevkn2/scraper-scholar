from typing import Optional
from pydantic import BaseModel


class CookieData(BaseModel):
    name: str
    value: str
    domain: Optional[str] = None
    path: Optional[str] = None
    expires: Optional[int] = None
    secure: bool = False
    http_only: bool = False
