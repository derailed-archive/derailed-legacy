from typing import Any, Generator
import pytest
from derailed.app import app
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as tc:
        yield tc


@pytest.fixture
def token(client: TestClient) -> Generator[str, Any, None]:
    r = client.post('/register', json={'username': 'test', 'email': 'test@testing.io', 'password': 'abcdefghi12345678'})
    return r.json()['token']
