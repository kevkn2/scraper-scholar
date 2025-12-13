from abc import ABC, abstractmethod

from app.domain.entities.oauth import OAuthToken, RefreshOAuthToken, RequestOAuthToken


class TokenProvider(ABC):
    @abstractmethod
    def get_token(self, request_input: RequestOAuthToken) -> OAuthToken:
        pass

    @abstractmethod
    def use_access_token(self) -> OAuthToken:
        pass

    @abstractmethod
    def refresh_token(self, refresh_input: RefreshOAuthToken) -> OAuthToken:
        pass
