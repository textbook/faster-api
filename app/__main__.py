import os

import uvicorn
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI

from app.container import RootContainer


@inject
def main(app: FastAPI = Provide[RootContainer.app]):
    uvicorn.run(
        app,
        host=os.getenv("HOST", "localhost"),
        port=int(os.getenv("PORT", 8080)),
    )


if __name__ == "__main__":
    container = RootContainer()
    container.wire(modules=[__name__])
    main()
