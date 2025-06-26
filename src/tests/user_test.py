from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.main.app.core.config.config_manager import load_config
from src.main.app.server import app

configs = load_config().server


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.parametrize(
    "endpoint, test_data, expected_status_code",
    [
        (
            "login",
            {
                "username": "example_user",
                "password": "example_password_error",
            },
            HTTPStatus.UNAUTHORIZED,
        ),
    ],
)
def test_user_login_error(client, endpoint, test_data, expected_status_code):
    url = f"{configs.api_version}/user/{endpoint}"
    response = client.post(
        url,
        data=test_data,
    )
    assert response.status_code == expected_status_code
