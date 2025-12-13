import requests
from app.domain.entities.oauth import OAuthToken, RequestOAuthToken
from app.domain.port.oauth import TokenProvider
from app.repositories.oauth_token_repository import OAuthTokenRepository

# from app.exception.token_provider import FailedToGetTokenException


class MendeleyTokenProvider(TokenProvider):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        token_url: str,
        oauth_token_repository: OAuthTokenRepository,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_url = token_url
        self.oauth_token_repository = oauth_token_repository

    async def get_token(self, request_input: RequestOAuthToken) -> OAuthToken:
        response = requests.post(
            self.token_url,
            data=request_input.model_dump(),
            auth=(self.client_id, self.client_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10,
        )

        print(response.status_code)

        # if response.status_code != 200:
        #     FailedToGetTokenException()

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


def new_mendeley_token_provider(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    token_url: str,
    oauth_token_repository: OAuthTokenRepository,
) -> MendeleyTokenProvider:
    return MendeleyTokenProvider(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        token_url=token_url,
        oauth_token_repository=oauth_token_repository,
    )
