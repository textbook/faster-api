class MessagesService:

    _message: str
    """The message to show the world."""

    def __init__(self, message: str):
        self._message = message

    def get_message(self) -> str:
        return self._message
