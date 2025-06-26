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
"""Database configuration for the application."""

from src.main.app.core.utils import alembic_config_util


class DatabaseConfig:
    def __init__(
        self,
        url: str,
        pool_size: int,
        max_overflow: int,
        pool_recycle: int,
        echo_sql: bool,
        pool_pre_ping: bool,
        enable_redis: bool,
        cache_host: str,
        cache_port: int,
        cache_pass: str,
        db_num: int,
        dialect: str = None,
    ) -> None:
        """
        Initializes database configuration.

        Args:
            dialect: The model of database.
            url: The url of database.
            pool_size: The pool size of database.
            max_overflow: The max overflow of database.
            pool_recycle: The pool recycle of database.
            echo_sql: Whether to echo sql statements.
            pool_pre_ping: Whether to pre ping.
            enable_redis: Whether to enable Redis cache.
            cache_host: Redis host address.
            cache_port: Redis port number.
            cache_pass: Redis password.
            db_num: Redis database number.
        """
        if dialect is None or len(dialect.strip()) == 0:
            dialect = alembic_config_util.get_db_dialect()
        self.dialect = dialect
        if url is None or len(url.strip()) == 0:
            url = alembic_config_util.get_db_url()
        self.url = url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_recycle = pool_recycle
        self.echo_sql = echo_sql
        self.pool_pre_ping = pool_pre_ping
        self.enable_redis = enable_redis
        self.cache_host = cache_host
        self.cache_port = cache_port
        self.cache_pass = cache_pass
        self.db_num = db_num

    def __str__(self) -> str:
        """
        Returns a string representation of the database configuration.

        Returns:
            A string representation of the DatabaseConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
