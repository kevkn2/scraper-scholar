import secrets
from urllib.parse import urlencode

from app.domain.port.usecase import Usecase


class LoginUsecase(Usecase[None, str]):
    def __init__(self, client_id: str, redirect_uri: str):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.MENDELEY_AUTH_URL = "https://api.mendeley.com/oauth/authorize"
        self.state = secrets.token_urlsafe(16)

    async def execute(self, input_dto: None) -> str:
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "all",
            "state": self.state,
        }

        url = f"{self.MENDELEY_AUTH_URL}?{urlencode(params)}"
        return url


def new_login_usecase(client_id: str, redirect_uri: str) -> LoginUsecase:
    return LoginUsecase(client_id=client_id, redirect_uri=redirect_uri)
