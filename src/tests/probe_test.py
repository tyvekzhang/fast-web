import pytest
from fastapi.testclient import TestClient

from src.main.app.core.config.config_manager import load_config
from src.main.app.server import app

configs = load_config()
server_config = configs.server

client = TestClient(app)


@pytest.mark.parametrize(
    "endpoint,expected_json",
    [
        ("liveness", {"code": 0, "message": "Hi"}),
    ],
)
def test_probe(endpoint, expected_json):
    response = client.get(f"{server_config.api_prefix}/probe/{endpoint}")
    assert response.status_code == 200
    assert response.json() == expected_json
