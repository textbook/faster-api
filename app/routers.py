from dependency_injector import containers, providers

from app.health import create_health_router
from app.messages import create_messages_router, MessagesController


class Routers(containers.DeclarativeContainer):
    messages_controller = providers.Dependency(instance_of=MessagesController)
    all_routers = providers.List(
        providers.Factory(
            create_messages_router,
            controller=messages_controller
        ),
        providers.Factory(create_health_router),
    )
