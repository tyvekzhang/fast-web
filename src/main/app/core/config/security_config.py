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
"""Security configuration for the application."""


class SecurityConfig:
    def __init__(
        self,
        enable: bool,
        enable_swagger: bool,
        algorithm: str,
        secret_key: str,
        access_token_expire_minutes: int,
        refresh_token_expire_minutes: int,
        white_list_routes: str,
        backend_cors_origins: str,
        black_ip_list: str,
    ) -> None:
        """
        Initializes security configuration.

        Args:
            enable: Whether to enable security.
            enable_swagger: Whether to enable swagger ui.
            algorithm: The encryption algorithm used for token generation.
            secret_key: The secret key used for signing the tokens.
            access_token_expire_minutes: The number of minutes until the access token expires.
            refresh_token_expire_minutes: The number of minutes until the refresh token expires.
            white_list_routes: Comma-separated list of routes which can be accessed without authentication.
            backend_cors_origins: Comma-separated list of allowed CORS origins.
            black_ip_list: Comma-separated list of blocked IP addresses.
        """
        self.enable = enable
        self.enable_swagger = enable_swagger
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_minutes = refresh_token_expire_minutes
        self.white_list_routes = white_list_routes
        self.backend_cors_origins = backend_cors_origins
        self.black_ip_list = black_ip_list

    def __str__(self) -> str:
        """
        Returns a string representation of the security configuration.

        Returns:
            A string representation of the SecurityConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
