from http import HTTPStatus

from fastapi.testclient import TestClient

from app import app


def test_get_health():
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_message():
    client = TestClient(app)
    response = client.get("/messages/first")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello, world!"}
