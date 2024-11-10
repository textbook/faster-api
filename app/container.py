import os

from dependency_injector import containers, providers
from fastapi import APIRouter, FastAPI

from app.routers import Routers

def create_app(routers: list[APIRouter]) -> FastAPI:
    app = FastAPI()
    for router in routers:
        app.include_router(router)
    return app


class Container(containers.DeclarativeContainer):
    message = providers.Object(os.getenv("MESSAGE", "Hello, world!"))
    routers = providers.Container(Routers)
    app = providers.Factory(
        create_app,
        routers=routers.all_routers,
    )
