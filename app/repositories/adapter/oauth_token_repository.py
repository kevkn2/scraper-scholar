from datetime import datetime, timedelta
from typing import Optional
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.oauth_token import OAuthTokenModel
from app.repositories.interfaces import IOAuthTokenRepository


class OAuthTokenRepository(IOAuthTokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_token(
        self,
        provider: str,
        access_token: str,
        refresh_token: str | None,
        expires_in: int,
        scope: str | None = None,
    ) -> OAuthTokenModel:
        expires_at = datetime.now() + timedelta(seconds=expires_in)

        token = await self.get_by_provider(provider)

        if token:
            token.access_token = access_token
            token.refresh_token = refresh_token
            token.expires_at = expires_at
            token.scope = scope
        else:
            token = OAuthTokenModel(
                id=str(uuid.uuid4()),
                provider=provider,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at,
                scope=scope,
            )
            self.session.add(token)

        await self.session.commit()
        return token

    async def get_by_provider(self, provider: str) -> Optional[OAuthTokenModel]:
        stmt = select(OAuthTokenModel).where(OAuthTokenModel.provider == provider)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_tokens(
        self,
        provider: str,
        access_token: str,
        refresh_token: str | None,
        expires_in: int,
    ) -> None:
        token = await self.get_by_provider(provider)

        token.access_token = access_token
        token.refresh_token = refresh_token
        token.expires_at = datetime.now() + timedelta(seconds=expires_in)

        await self.session.commit()


def new_oauth_token_repository(session: AsyncSession) -> OAuthTokenRepository:
    return OAuthTokenRepository(session=session)
