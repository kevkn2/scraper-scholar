from typing import List

import requests
from app.domain.entities.mendeley.reference_manager import (
    Author,
    Identifiers,
    MendeleyDocument,
)
from app.domain.port.oauth import TokenProvider
from app.domain.port.reference_manager import ReferenceManager


class MendeleyManager(ReferenceManager[MendeleyDocument]):
    def __init__(
        self,
        token_provider: TokenProvider,
    ):
        self.token_provider = token_provider

    async def _get_access_token(self) -> str:
        token = await self.token_provider.use_access_token()
        return token.access_token

    async def get_documents(self) -> List[MendeleyDocument]:
        access_token = await self._get_access_token()
        r = requests.get(
            "https://api.mendeley.com/documents",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.mendeley-document.1+json",
            },
            timeout=10,
        )
        r.raise_for_status()

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
