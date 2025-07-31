"""Thread-safe async SQLAlchemy engine management."""

from threading import Lock
from typing import Dict, Union

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from sqlmodel import select
from src.main.app.core.session.db_session import db_session
from src.main.app.core.utils.alembic_config_util import get_sqlite_db_path

from src.main.app.core.config import config_manager
from src.main.app.mapper.codegen.connection_mapper import connectionMapper
from src.main.app.mapper.codegen.database_mapper import databaseMapper
from src.main.app.model.codegen.connection_model import ConnectionModel
from src.main.app.model.codegen.database_model import DatabaseModel

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


async def get_cached_async_engine(
    *,
    connection_id: Union[str, int] = None,
    database_id: Union[str, int] = None,
) -> AsyncEngine:
    """
    Get or create an AsyncEngine instance based on the URL.
    Uses thread-safe singleton pattern to cache engines.

    Args:
        connection_id: Database connection id.
        database_id: Database id.

    Returns:
        AsyncEngine: SQLAlchemy async engine instance
    """
    global _engine_map

    cache_key = str(connection_id) + str(database_id)

    # Return cached engine if exists
    with _lock:
        if cache_key in _engine_map:
            return _engine_map[cache_key]
        database: DatabaseModel = await databaseMapper.select_by_id(id=database_id)
        if database is not None:
            connection_id = database.connection_id
        connection: ConnectionModel = await connectionMapper.select_by_id(id=connection_id)
        if connection is None:
            pass
        url = get_database_url(database, connection)

        # Create new engine if not cached
        new_engine = create_async_engine(url=url, poolclass=NullPool)

        # Cache the new engine
        _engine_map[cache_key] = new_engine
        return new_engine


async def clear_engine_cache() -> None:
    """
    Clear all cached engine instances.
    Should be called when shutting down the application.
    """
    global _engine_map
    with _lock:
        for engine in _engine_map.values():
            await engine.dispose()
        _engine_map.clear()


async def get_engine_by_database_id(*, env: str, database_id: int):
    async with db_session(env=env) as session:
        statement = select(DatabaseModel).where(DatabaseModel.id == database_id)
        exec_response = await session.exec(statement)
        database: DatabaseModel = exec_response.one_or_none()
        if database is None:
            pass
        statement = select(ConnectionModel).where(ConnectionModel.id == database.connection_id)
        exec_response = await session.exec(statement)
        connection: ConnectionModel = exec_response.one_or_none()
        if connection is None:
            pass
        url = get_database_url(database, connection)
        engine = create_async_engine(
            url=url,
        )
        return engine


def get_database_url(database: DatabaseModel, connection: ConnectionModel) -> str:
    database_type = connection.database_type
    database_type = database_type.lower()
    if database_type == "sqlite":
        url = get_sqlite_db_path()
    elif database_type == "mysql":
        host = connection.host
        port = connection.port
        username = connection.username
        password = connection.password
        url = f"mysql+aiomysql://{username}:{password}@{host}:{port}"
        if database is not None:
            url = str(url) + "/" + database.database_name
    elif database_type == "postgresql" or database_type == "pgsql":
        host = connection.host
        port = connection.port
        username = connection.username
        password = connection.password
        url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}"
        if database is not None:
            url = str(url) + "/" + database.database_name
        else:
            url = str(url) + "/" + connection.connection_database
    else:
        pass
    return url
