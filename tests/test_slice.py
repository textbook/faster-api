from http import HTTPStatus
from typing import Callable
from unittest.mock import Mock

from dependency_injector import providers
from fastapi.testclient import TestClient

from app.container import RootContainer
from app.messages.messages_service import MessagesService


def test_app_slice():
    container = RootContainer()
    container.services.messages.override(providers.Object(Mock(spec=MessagesService)))
    client = TestClient(container.app())
    mock_messages_service = container.services.messages()
    mock_messages_service.get_message.return_value = "Nothing"

    response = client.get("/messages/first")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == dict(message="Nothing")
    mock_messages_service.get_message.assert_called_once_with()
