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
