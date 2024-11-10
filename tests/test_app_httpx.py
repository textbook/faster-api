from http import HTTPStatus

import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_health(httpx_client: AsyncClient):
    response = await httpx_client.get("/healthz")
    assert response.status_code == HTTPStatus.NO_CONTENT
