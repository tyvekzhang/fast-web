import pytest
from fastapi.testclient import TestClient

from src.main.app.core.config.config_manager import load_config


@pytest.fixture
def client():
    from src.main.app.server import app

    return TestClient(app)


@pytest.mark.parametrize(
    "endpoint,expected_json",
    [
        ("liveness", {"code": 0, "msg": "Hi"}),
    ],
)
def test_probe(client, endpoint, expected_json):
    response = client.get(
        f"{load_config().server.api_version}/probe/{endpoint}"
    )
    assert response.status_code == 200
    assert response.json() == expected_json
