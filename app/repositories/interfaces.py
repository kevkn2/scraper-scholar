from abc import ABC, abstractmethod
from typing import Dict, Optional

from app.models.oauth_token import OAuthTokenModel


class IOAuthTokenRepository(ABC):
    @abstractmethod
    def upsert_token(
        self,
        provider: str,
        access_token: str,
        refresh_token: str | None,
        expires_in: int,
        scope: str | None = None,
    ) -> OAuthTokenModel:
        pass

    @abstractmethod
    def get_by_provider(self, provider: str) -> Optional[OAuthTokenModel]:
        pass

    @abstractmethod
    def update_tokens(
        self,
        provider: str,
        access_token: str,
        refresh_token: str | None,
        expires_in: int,
    ) -> None:
        pass


class IScholarCookieRepository(ABC):
    @abstractmethod
    def get_cookies(self) -> Optional[Dict[str, str]]:
        pass

    @abstractmethod
    def save_cookies(self, cookies: Dict[str, str], ttl: int = 3600) -> None:
        pass

    @abstractmethod
    def delete_cookies(self) -> None:
        pass
