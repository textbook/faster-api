from app.messages.messages_models import Message
from app.messages.messages_router import MessagesController
from app.messages.messages_service import MessagesService


class MessagesControllerImpl(MessagesController):

    _service: MessagesService

    def __init__(self, service: MessagesService):
        self._service = service

    def get_first_message(self) -> Message:
        message = self._service.get_message()
        return Message(message=message)
