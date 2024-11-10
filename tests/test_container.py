from http import HTTPStatus

from requests import Session

def test_get_healthz(requests_session: Session):
    response = requests_session.get("/healthz")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_message(requests_session: Session):
    response = requests_session.get("/messages/first")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello, world!"}
