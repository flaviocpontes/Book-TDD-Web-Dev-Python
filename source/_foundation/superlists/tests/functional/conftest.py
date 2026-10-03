import asyncio
import socket
import threading
import time

import pytest
from hypercorn.asyncio import serve
from hypercorn.config import Config

from superlists import app


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _wait_until_listening(port: int, timeout: float = 5) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
            return
        except OSError:
            time.sleep(0.05)
    raise RuntimeError(f"server did not start listening on port {port}")


@pytest.fixture(scope="session")
def live_server_url():
    port = _free_port()
    config = Config()
    config.bind = [f"127.0.0.1:{port}"]

    loop = asyncio.new_event_loop()
    stop = asyncio.Event()

    def run_server():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(serve(app, config, shutdown_trigger=stop.wait))

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    _wait_until_listening(port)

    yield f"http://127.0.0.1:{port}"

    loop.call_soon_threadsafe(stop.set)
    thread.join(timeout=5)


@pytest.fixture(scope="session")
def base_url(live_server_url):
    # pytest-playwright's page.goto("/") resolves against this
    return live_server_url
