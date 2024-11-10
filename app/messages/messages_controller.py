from app.messages.messages_models import Message
from app.messages.messages_router import MessagesController


class MessagesControllerImpl(MessagesController):

    _message: str
    """The message to show the world."""

    def __init__(self, message: str):
        self._message = message

    def get_first_message(self) -> Message:
        return Message(message=self._message)
