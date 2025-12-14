import json
from typing import Dict, Optional
from app.database.redis import async_redis_client
from app.repositories.interfaces import IScholarCookieRepository


class ScholarCookieRepository(IScholarCookieRepository):
    def __init__(self, key_prefix: str = "scholar_cookies"):
        self.key_prefix = key_prefix

    async def get_cookies(self) -> Optional[Dict[str, str]]:
        cookies_json = await async_redis_client.get(self.key_prefix)
        if cookies_json:
            return json.loads(cookies_json)
        return None

    async def save_cookies(self, cookies: Dict[str, str], ttl: int = 3600) -> None:
        cookies_json = json.dumps(cookies)
        await async_redis_client.setex(self.key_prefix, ttl, cookies_json)

    async def delete_cookies(self) -> None:
        await async_redis_client.delete(self.key_prefix)


def new_scholar_cookie_repository():
    return ScholarCookieRepository()
