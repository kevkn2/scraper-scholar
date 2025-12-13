from pydantic import BaseModel


class RequestOAuthToken(BaseModel):
    code: str
    grant_type: str
    redirect_uri: str


class RefreshOAuthToken(BaseModel):
    refresh_token: str
    grant_type: str


class OAuthToken(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
