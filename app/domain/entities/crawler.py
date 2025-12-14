from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel

from app.domain.entities.http import CookieData


class FetchInput(BaseModel):
    url: str
    method: str
    headers: Optional[Dict[str, str]] = None
    data: Optional[Dict[str, Any]] = None
    cookies: List[CookieData] = []


class FetchOutput(BaseModel):
    status_code: int
    headers: Dict[str, str]
    data: str
    cookies: List[CookieData] = []
