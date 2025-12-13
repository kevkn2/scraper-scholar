from typing import Any, Callable, Dict, Optional
import httpx

from app.config import settings
from app.domain.entities.oauth import OAuthToken


async def request_with_refresh(
    url: str,
    method: str,
    refresh_callback: Callable[[], OAuthToken],
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url, headers=headers, data=data)

        if response.status_code == 401:
            new_token = await refresh_callback()

            headers["Authorization"] = f"Bearer {new_token.access_token}"

            response = await client.request(method, url, headers=headers, data=data)

        response.raise_for_status()
        return response


async def request_token(
    auth: httpx.Auth,
    data: Optional[Dict[str, Any]] = None,
) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=settings.MENDELEY_TOKEN_URL,
            data=data,
            auth=auth,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10,
        )

        response.raise_for_status()
        return response
