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
"""Server configuration for the application."""


class ServerConfig:
    def __init__(
        self,
        name: str,
        host: str,
        port: int,
        version: str,
        app_desc: str,
        api_version: str,
        workers: int,
        debug: bool,
        log_file_path: str,
        win_tz: str,
        linux_tz: str,
        enable_rate_limit: bool,
        global_default_limits: str,
    ) -> None:
        """
        Initializes server configuration.

        Args:
            host: The server host address.
            name: The server name.
            port: The server port number.
            version: The server version.
            app_desc: The server app_desc.
            api_version: The server api_version.
            debug: Whether to enable debug mode.
            workers: The server worker numbers.
            log_file_path: Path to the log file.
            win_tz: Windows timezone setting.
            linux_tz: Linux timezone setting.
            enable_rate_limit: Whether to enable rate limiting.
            global_default_limits: Global rate limit setting.
        """
        self.host = host
        self.name = name
        self.port = port
        self.version = version
        self.app_desc = app_desc
        self.api_version = api_version
        self.debug = debug
        self.workers = workers
        self.log_file_path = log_file_path
        self.win_tz = win_tz
        self.linux_tz = linux_tz
        self.enable_rate_limit = enable_rate_limit
        self.global_default_limits = global_default_limits

    def __str__(self) -> str:
        """
        Returns a string representation of the server configuration.

        Returns:
            A string representation of the ServerConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
