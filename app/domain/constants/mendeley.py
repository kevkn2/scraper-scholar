from app.config import settings


MENDELEY_REDIRECT_URL = f"{settings.SERVER_URL}/v1/mendeley/oauth/callback"
MENDELEY_TOKEN_URL = "https://api.mendeley.com/oauth/token"
