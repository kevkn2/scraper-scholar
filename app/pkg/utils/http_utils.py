from typing import Dict, List
import httpx

from app.domain.entities.http import CookieData


def normalize_cookies(cookies: httpx.Cookies) -> List[CookieData]:
    result = []

    for c in cookies.jar:
        result.append(
            CookieData(
                name=c.name,
                value=c.value,
                domain=c.domain,
                path=c.path,
                expires=c.expires,
                secure=c.secure,
                http_only=c.has_nonstandard_attr("HttpOnly"),
            )
        )
    return result


def get_to_httpx_cookies(cookies: List[CookieData]) -> httpx.Cookies:
    jar = httpx.Cookies()
    for c in cookies:
        jar.set(
            name=c.name,
            value=c.value,
            domain=c.domain,
            path=c.path,
        )
    return jar


def create_list_cookies_data(cookies: Dict[str, str]) -> List[CookieData]:
    result = []

    for cookie in cookies.values():
        result.append(
            CookieData(
                name=cookie["name"],
                value=cookie["value"],
                domain=cookie["domain"],
                path=cookie["path"],
            )
        )

    return result
