from http import HTTPStatus

from fastapi import APIRouter

def create_health_router() -> APIRouter:
    router = APIRouter(prefix="/healthz")

    @router.get("", status_code=HTTPStatus.NO_CONTENT)
    def _() -> None:
        return None

    return router
