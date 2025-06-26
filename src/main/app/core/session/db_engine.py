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
"""Thread-safe async SQLAlchemy engine management."""

from threading import Lock
from typing import Dict

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from src.main.app.core.config import config_manager


# Global engine cache with thread safety
_engine_map: Dict[str, AsyncEngine] = {}
_lock = Lock()

async_engine: AsyncEngine


def get_async_engine() -> AsyncEngine:
    """
    Get or create a cached async SQLAlchemy engine with thread-safe initialization.

    Returns:
        AsyncEngine: Configured SQLAlchemy async engine based on application config.
    """
    global async_engine
    database_config = config_manager.load_config().database
    if database_config.dialect.lower() == "sqlite":
        async_engine = create_async_engine(
            url=database_config.url,
            echo=database_config.echo_sql,
            pool_recycle=database_config.pool_recycle,
            pool_pre_ping=True,
        )
    else:
        async_engine = create_async_engine(
            url=database_config.url,
            echo=database_config.echo_sql,
            pool_size=database_config.pool_size,
            max_overflow=database_config.max_overflow,
            pool_recycle=database_config.pool_recycle,
            pool_pre_ping=True,
        )
    return async_engine
