# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    url = f"{configs.api_prefix}/user/{endpoint}"
    response = client.post(
        url,
        data=test_data,
    )
    assert response.status_code == expected_status_code
