# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
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
#
"""Configuration loading and management."""

import os
from functools import lru_cache

from src.main.app.core import constant
from src.main.app.core.config.config import (
    Config,
)
from src.main.app.core.config.config_loader import ConfigLoader
from src.main.app.core.config.database_config import DatabaseConfig
from src.main.app.core.config.security_config import SecurityConfig
from src.main.app.core.config.server_config import ServerConfig

config: Config


@lru_cache
def load_config() -> Config:
    """
    Loads the configuration based on the provided command-line arguments.

    Returns:
        Config: A configuration object populated with the loaded settings.
    """
    global config
    env = os.getenv(constant.ENV, "dev")

    config_file = os.getenv(constant.CONFIG_FILE, None)
    config_loader = ConfigLoader(env, config_file)
    config_dict = config_loader.load_config()
    config = Config(config_dict)
    return config


@lru_cache
def load_server_config() -> ServerConfig:
    """
    Loads and returns the server configuration.

    Returns:
        ServerConfig: The server configuration object.
    """
    config_data = load_config()
    return config_data.server


@lru_cache
def load_database_config() -> DatabaseConfig:
    """
    Loads and returns the database configuration.

    Returns:
        DatabaseConfig: The database configuration object.
    """
    config_data = load_config()
    return config_data.database


@lru_cache
def load_security_config() -> SecurityConfig:
    """
    Loads and returns the security configuration.

    Returns:
        SecurityConfig: The security configuration object.
    """
    config_data = load_config()
    return config_data.security


def get_database_url(*, env: str = "dev"):
    """
    Retrieves the database URL from the configuration file for the specified environment.

    Returns:
        str: The database URL string from the configuration file.
    """

    assert env in ("dev", "prod", "local")
    config_path = os.path.join(constant.RESOURCE_DIR, f"config-{env}.yml")
    config_dict = ConfigLoader.load_yaml_file(config_path)
    if "database" not in config_dict:
        raise ValueError(
            CommonCode.PARAMETER_ERROR.code,
            f"{CommonCode.PARAMETER_ERROR.msg}: {env}",
        )
    return config_dict["database"]["url"]
