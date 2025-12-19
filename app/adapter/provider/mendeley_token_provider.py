from app.domain.entities.oauth import OAuthToken, RefreshOAuthToken, RequestOAuthToken
from app.domain.port.oauth import TokenProvider
from app.pkg.utils.request_utils import request_token
from app.repositories.interfaces import IOAuthTokenRepository


class MendeleyTokenProvider(TokenProvider):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        token_url: str,
        oauth_token_repository: IOAuthTokenRepository,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_url = token_url
        self.oauth_token_repository = oauth_token_repository

    async def get_token(self, request_input: RequestOAuthToken) -> OAuthToken:
        response = await request_token(
            data=request_input.model_dump(),
            auth=(self.client_id, self.client_secret),
        )

        payload = response.json()
        await self.oauth_token_repository.upsert_token(
            provider="mendeley",
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            expires_in=payload["expires_in"],
        )
        return OAuthToken(
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            expires_in=payload["expires_in"],
        )

    async def use_access_token(self):
        oauth_token = await self.oauth_token_repository.get_by_provider("mendeley")
        return OAuthToken(
            access_token=oauth_token.access_token,
            refresh_token=oauth_token.refresh_token,
            expires_in=oauth_token.expires_at.timetuple().tm_sec,
        )

    async def refresh_token(self, refresh_input: RefreshOAuthToken) -> OAuthToken:
        response = await request_token(
            data=refresh_input.model_dump(),
            auth=(self.client_id, self.client_secret),
        )

        payload = response.json()
        await self.oauth_token_repository.update_tokens(
            provider="mendeley",
            access_token=payload["access_token"],
            refresh_token=payload.get("refresh_token"),
            expires_in=payload["expires_in"],
        )

        return OAuthToken(
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            expires_in=payload["expires_in"],
        )


def new_mendeley_token_provider(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    token_url: str,
    oauth_token_repository: IOAuthTokenRepository,
):
    return MendeleyTokenProvider(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        token_url=token_url,
        oauth_token_repository=oauth_token_repository,
    )
