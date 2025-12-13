from app.domain.entities.oauth import RequestOAuthToken
from app.domain.port.usecase import Usecase
from app.domain.port.oauth import TokenProvider
from app.usecase.mendeley.dto import RedirectInputDTO, RedirectOutputDTO


class RedirectUsecase(Usecase[RedirectInputDTO, RedirectOutputDTO]):
    def __init__(
        self,
        token_provider: TokenProvider,
        redirect_uri: str,
    ):
        self.token_provider = token_provider
        self.redirect_uri = redirect_uri

    async def execute(self, input_dto: RedirectInputDTO) -> RedirectOutputDTO:
        request_oauth_token = RequestOAuthToken(
            code=input_dto.code,
            grant_type="authorization_code",
            redirect_uri=self.redirect_uri,
        )

        oauth_token = await self.token_provider.get_token(request_oauth_token)

        return RedirectOutputDTO(
            access_token=oauth_token.access_token,
            refresh_token=oauth_token.refresh_token,
            expires_in=oauth_token.expires_in,
        )


def new_redirect_usecase(
    TokenProvider: TokenProvider,
    redirect_uri: str,
) -> RedirectUsecase:
    return RedirectUsecase(
        token_provider=TokenProvider,
        redirect_uri=redirect_uri,
    )
