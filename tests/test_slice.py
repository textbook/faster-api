from http import HTTPStatus
from typing import Callable
from unittest.mock import Mock

from dependency_injector import providers
from fastapi.testclient import TestClient

from app.container import Container
from app.messages import MessagesController
from app.messages.messages_models import Message


def test_app_slice():
    mock_messages_controller = Mock(spec=MessagesController)
    client = client_with_override(
        lambda c: c.routers.messages_controller.override(
            providers.Factory(lambda: mock_messages_controller),
        ),
    )
    mock_messages_controller.get_first_message.return_value = Message(
        message="Nothing"
    )
    response = client.get("/messages/first")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == dict(message="Nothing")
    mock_messages_controller.get_first_message.assert_called_once_with()


def client_with_override(override: Callable[[Container], None]) -> TestClient:
    container = Container()
    override(container)
    container.init_resources()
    return TestClient(container.app())
