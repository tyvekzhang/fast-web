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
"""Application Configuration."""

from src.main.app.core.config.database_config import DatabaseConfig
from src.main.app.core.config.security_config import SecurityConfig
from src.main.app.core.config.server_config import ServerConfig


class Config:
    def __init__(self, config_dict=None):
        if "server" in config_dict:
            self.server = ServerConfig(**config_dict["server"])
        else:
            self.server = ServerConfig()
        if "database" in config_dict:
            self.database = DatabaseConfig(**config_dict["database"])
        else:
            self.database = DatabaseConfig()
        if "security" in config_dict:
            self.security = SecurityConfig(**config_dict["security"])
        else:
            self.security = SecurityConfig()

    def __str__(self) -> str:
        """
        Returns a string representation of the configuration.

        Returns:
            A string representation of the config instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
