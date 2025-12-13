from app.domain.entities.mendeley.reference_manager import MendeleyDocument
from app.domain.port.reference_manager import ReferenceManager
from app.domain.port.usecase import Usecase
from app.usecase.mendeley.dto import ListDocumentsInputDTO, ListDocumentsOutputDTO


class MendeleyListDocumentsUseCase(
    Usecase[ListDocumentsInputDTO, ListDocumentsOutputDTO[MendeleyDocument]]
):
    def __init__(self, mendeley_manager: ReferenceManager[MendeleyDocument]):
        self.mendeley_manager = mendeley_manager

    async def execute(
        self, input_dto: ListDocumentsInputDTO
    ) -> ListDocumentsOutputDTO[MendeleyDocument]:
        documents = await self.mendeley_manager.get_documents()

        return ListDocumentsOutputDTO[MendeleyDocument](documents=documents)


def new_list_documents_usecase(
    mendeley_manager: ReferenceManager[MendeleyDocument],
) -> MendeleyListDocumentsUseCase:
    return MendeleyListDocumentsUseCase(
        mendeley_manager=mendeley_manager,
    )
