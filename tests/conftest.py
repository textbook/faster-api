from __future__ import annotations

import typing as tp
from contextlib import suppress
from pathlib import Path
from socket import socket
from threading import Thread
from time import sleep

import httpx
import pytest
import requests
from docker import DockerClient
from docker.errors import APIError, BuildError
from docker.models.containers import Container
from docker.models.images import Image
from fastapi import FastAPI
from uvicorn import Config, Server

from app.container import RootContainer

client = DockerClient.from_env()

Status = tp.Literal["created", "restarting", "running", "removing", "paused", "exited", "dead"]


class Binding(tp.TypedDict):
    HostIp: str
    HostPort: str


class TestSession(requests.Session):
    """Prepends the base URL and disables redirect following."""

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self._base_url = base_url

    def prepare_request(
        self,
        request: requests.Request
    ) -> requests.PreparedRequest:
        request.url = f"{self._base_url}{request.url}"
        return super().prepare_request(request)

    def send(
        self,
        request: requests.PreparedRequest,
        **kwargs,
    ) -> requests.Response:
        kwargs["allow_redirects"] = False
        return super().send(request, **kwargs)


@pytest.fixture
def requests_session(base_url: str) -> requests.Session:
    return TestSession(base_url)


@pytest.fixture(scope="module")
def image() -> Image:
    root = Path(__file__).parent / ".."
    logs = []
    try:
        (image, logs) = client.images.build(path=str(root))
    except BuildError as exc:
        logs = exc.build_log
        raise exc
    finally:
        for event in logs:
            if "stream" in event:
                print(event["stream"], end="")
            else:
                print(event)
    return image


@pytest.fixture(scope="module")
def container(image: Image, request: pytest.FixtureRequest) -> Container:
    container: Container = client.containers.run(
        image,
        detach=True,
        ports={"8000/tcp": None},
    )
    request.addfinalizer(create_cleanup(container))
    return container


@pytest.fixture(scope="module")
def base_url(container: Container) -> str:
    wait_for_healthy(container)
    return get_base_url(container, "8000/tcp")


@pytest.fixture(scope="module")
async def httpx_client() -> tp.Generator[httpx.AsyncClient, None, None]:
    with TestServer.random_port(RootContainer().app()) as server:
        async with httpx.AsyncClient(base_url=server.url) as client_:
            yield client_


class TestServer:

    @classmethod
    def random_port(cls, application: FastAPI) -> TestServer:
        socket_ = socket()
        socket_.bind(("", 0))
        return cls(application, socket_)

    def __init__(self, application: FastAPI, socket_: socket):
        self._server = Server(Config(app=application))
        self._socket = socket_
        self._thread = Thread(
            target=self._server.run,
            kwargs=dict(sockets=[self._socket]),
        )

    def __enter__(self) -> TestServer:
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._server.should_exit = True
        self._thread.join()

    @property
    def url(self) -> str:
        host, port = self._socket.getsockname()
        return f"http://{host}:{port}"

def create_cleanup(container: Container) -> tp.Callable[[], None]:
    def cleanup():
        container.reload()
        print(container.logs().decode("utf-8"))
        with suppress(APIError):
            container.stop()
        container.remove()
    return cleanup


def get_base_url(
    container: Container,
    binding: tp.Optional[str] = None,
) -> tp.Optional[str]:
    container.reload()
    if ports := container.ports:
        if bindings := (
            ports[binding]
            if binding is not None
            else next(iter(ports.values()))
        ):
            binding: Binding = bindings[0]
            return f"http://{binding['HostIp']}:{binding['HostPort']}"


def wait_for_healthy(
    container,
    *,
    delay: float = 0.1,
    retries: int = 20,
) -> None:
    for _ in range(retries):
        if url := get_base_url(container):
            with suppress(requests.exceptions.RequestException):
                if requests.get(f"{url}/healthz").ok:
                    break
        sleep(delay)
    else:
        raise Exception("container never became healthy")
