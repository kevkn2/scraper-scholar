from typing import List

from app.domain.entities.mendeley.reference_manager import (
    Author,
    Identifiers,
    MendeleyDocument,
)
from app.domain.entities.oauth import OAuthToken, RefreshOAuthToken
from app.domain.port.oauth import TokenProvider
from app.domain.port.reference_manager import ReferenceManager
from app.utils.request_utils import request_with_refresh


class MendeleyManager(ReferenceManager[MendeleyDocument]):
    def __init__(
        self,
        token_provider: TokenProvider,
    ):
        self.token_provider = token_provider

    async def _get_access_token(self) -> OAuthToken:
        token = await self.token_provider.use_access_token()
        return token

    async def _refresh_access_token(self, existing_token: OAuthToken) -> OAuthToken:
        new_token = await self.token_provider.refresh_token(
            RefreshOAuthToken(
                refresh_token=existing_token.refresh_token,
                grant_type="refresh_token",
            )
        )
        return new_token

    async def get_documents(self) -> List[MendeleyDocument]:
        token = await self._get_access_token()

        r = await request_with_refresh(
            url="https://api.mendeley.com/documents",
            method="GET",
            headers={
                "Authorization": f"Bearer {token.access_token}",
                "Accept": "application/vnd.mendeley-document.1+json",
            },
            refresh_callback=lambda: self._refresh_access_token(token),
        )

        return [
            MendeleyDocument(
                id=doc.get("id"),
                title=doc.get("title"),
                authors=[
                    Author(
                        first_name=a.get("first_name"),
                        last_name=a.get("last_name"),
                    )
                    for a in doc.get("authors", [])
                ],
                year=doc.get("year"),
                identifiers=Identifiers(
                    doi=doc.get("identifiers", {}).get("doi"),
                    isbn=doc.get("identifiers", {}).get("isbn"),
                    issn=doc.get("identifiers", {}).get("issn"),
                    pmid=doc.get("identifiers", {}).get("pmid"),
                    arxiv=doc.get("identifiers", {}).get("arxiv"),
                ),
            )
            for doc in r.json()
        ]


def new_mendeley_manager(
    token_provider: TokenProvider,
) -> MendeleyManager:
    return MendeleyManager(
        token_provider=token_provider,
    )
