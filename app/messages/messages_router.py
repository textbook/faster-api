from abc import abstractmethod, ABC

from fastapi import APIRouter

from app.messages.messages_models import Message


class MessagesController(ABC):

    @abstractmethod
    def get_first_message(self) -> Message: ...


def create_router(controller: MessagesController) -> APIRouter:
    router = APIRouter(prefix="/messages", tags=["messages"])

    @router.get("/first")
    def _() -> Message:
        return controller.get_first_message()

    return router
