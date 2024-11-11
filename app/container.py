from __future__ import annotations

import os

from dependency_injector import containers, providers
from fastapi import APIRouter, FastAPI

from app.messages.messages_controller import MessagesControllerImpl
from app.messages.messages_service import MessagesService
from app.routers import Routers

def create_app(routers: list[APIRouter]) -> FastAPI:
    app = FastAPI()
    for router in routers:
        app.include_router(router)
    return app


class RootContainer(containers.DeclarativeContainer):
    message = providers.Object(os.getenv("MESSAGE", "Hello, world!"))
    services = providers.Aggregate(
        messages=providers.Factory(MessagesService, message=message),
    )
    routers = providers.Container(
        Routers,
        messages_controller=providers.Factory(
            MessagesControllerImpl,
            service=services.messages,
        ),
    )
    app = providers.Factory(
        create_app,
        routers=routers.all_routers,
    )
