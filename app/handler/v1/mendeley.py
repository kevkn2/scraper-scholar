from typing import Optional
from fastapi.params import Depends
from fastapi.responses import RedirectResponse
from typing_extensions import Annotated
from fastapi import APIRouter

from app.adapter.mendeley.mendeley_manager import new_mendeley_manager
from app.config import settings
from app.adapter.mendeley.token_provider import new_mendeley_token_provider
from app.database.db_session import get_db_session
from app.domain.constants.mendeley import MENDELEY_REDIRECT_URL
from app.domain.entities.mendeley.reference_manager import MendeleyDocument
from app.domain.port.usecase import Usecase
from app.repositories.oauth_token_repository import new_oauth_token_repository
from app.usecase.mendeley.dto import (
    ListDocumentsInputDTO,
    ListDocumentsOutputDTO,
    RedirectInputDTO,
    RedirectOutputDTO,
)
from app.usecase.mendeley.list_documents import (
    new_list_documents_usecase,
)
from app.usecase.mendeley.login_usecase import LoginUsecase
from app.usecase.mendeley.redirect_usecase import new_redirect_usecase


v1_mendeley_router = APIRouter()


def get_redirect_usecase(session=Depends(get_db_session)):
    oauth_token_repository = new_oauth_token_repository(session)

    mendeley_token_provider = new_mendeley_token_provider(
        settings.MENDELEY_CLIENT_ID,
        settings.MENDELEY_CLIENT_SECRET,
        MENDELEY_REDIRECT_URL,
        settings.MENDELEY_TOKEN_URL,
        oauth_token_repository,
    )

    redirect_usecase = new_redirect_usecase(
        TokenProvider=mendeley_token_provider,
        redirect_uri=MENDELEY_REDIRECT_URL,
    )

    return redirect_usecase


def get_mendeley_list_documents_usecase(session=Depends(get_db_session)):
    oauth_token_repository = new_oauth_token_repository(session)

    mendeley_token_provider = new_mendeley_token_provider(
        settings.MENDELEY_CLIENT_ID,
        settings.MENDELEY_CLIENT_SECRET,
        MENDELEY_REDIRECT_URL,
        settings.MENDELEY_TOKEN_URL,
        oauth_token_repository,
    )

    mendeley_manager = new_mendeley_manager(
        token_provider=mendeley_token_provider,
    )

    list_documents_usecase = new_list_documents_usecase(
        mendeley_manager=mendeley_manager,
    )

    return list_documents_usecase


def get_mendeley_login_usecase():
    return LoginUsecase(
        client_id=settings.MENDELEY_CLIENT_ID,
        redirect_uri=MENDELEY_REDIRECT_URL,
    )


@v1_mendeley_router.get("/oauth/callback")
async def mendeley_oauth_callback(
    code: str,
    usecase: Annotated[
        Usecase[RedirectInputDTO, RedirectOutputDTO], Depends(get_redirect_usecase)
    ],
    state: Optional[str] = None,
):
    input_dto = RedirectInputDTO(code=code, state=state or "")
    output_dto = await usecase.execute(input_dto)

    print("OAuth Token Received:", output_dto)

    return output_dto


@v1_mendeley_router.get("/documents")
async def list_mendeley_documents(
    usecase: Annotated[
        Usecase[ListDocumentsInputDTO, ListDocumentsOutputDTO[MendeleyDocument]],
        Depends(get_mendeley_list_documents_usecase),
    ],
):
    input_dto = ListDocumentsInputDTO(page=1)
    output_dto = await usecase.execute(input_dto)

    return output_dto


@v1_mendeley_router.get("/login")
async def mendeley_login(
    usecase: Annotated[Usecase[None, str], Depends(get_mendeley_login_usecase)],
):
    url = await usecase.execute(None)
    return RedirectResponse(url)
