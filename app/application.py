from dependency_injector import providers

from app.container import Container
from app.messages.messages_controller import MessagesControllerImpl

container = Container()
container.routers.messages_controller.override(
    providers.Factory(
        MessagesControllerImpl,
        message=container.message,
    ),
)
container.init_resources()
app = container.app()
