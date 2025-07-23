from typing import Dict, Optional, Annotated

from fastapi import APIRouter, Query
from sqlmodel import inspect, text

from src.main.app.core import result
from src.main.app.core.result import HttpResponse
from src.main.app.core.session.db_engine import get_cached_async_engine
from src.main.app.mapper.database_mapper import databaseMapper
from src.main.app.model.db_database_model import DatabaseDO
from src.main.app.schema.common_schema import PageResult
from src.main.app.schema.database_schema import DatabaseAdd, DatabaseQuery
from src.main.app.service.database_service import DatabaseService
from src.main.app.service.impl.database_service_impl import DatabaseServiceImpl

database_router = APIRouter()
database_service: DatabaseService = DatabaseServiceImpl(mapper=databaseMapper)


@database_router.post("/database/create")
async def add_database(database_add: DatabaseAdd) -> HttpResponse[int]:
    """
    Database add.

    Args:
        database_add: Data required for add.

    Returns:
        BaseResponse with new database's ID.
    """
    record = DatabaseDO(**database_add.model_dump())
    database: DatabaseDO = await database_service.add(data=record)
    return HttpResponse(data=database.id)


@database_router.get("/database/databases")
async def list_databases(
    database_query: Annotated[DatabaseQuery, Query()],
) -> HttpResponse[PageResult]:
    """
    Filter databases with pagination.

    Args:
        database_query: Pagination and filter info to query

    Returns:
        BaseResponse with list and total count.
    """
    databases, total_count = await database_service.list_databases(
        data=database_query
    )

    return HttpResponse(
        data=PageResult(records=databases, total_count=total_count)
    )


@database_router.get("/database/version")
async def get_database_version(database_id: Optional[int] = None) -> Dict:
    engine = await get_cached_async_engine(database_id=database_id)
    async with engine.connect() as conn:
        dialect_name = engine.dialect.name.lower()
        if dialect_name == "sqlite":
            version_info = await conn.execute(text("SELECT sqlite_version();"))
        elif dialect_name in ("mysql", "mariadb"):
            version_info = await conn.execute(text("SELECT VERSION();"))
        elif dialect_name == "postgresql":
            version_info = await conn.execute(text("SELECT version();"))
        else:
            raise
        version = str((version_info.fetchone())[0]).split("-")[0]
    return result.success({"version_schema": f"{dialect_name}:{version}"})


@database_router.get("/database/{database_id}/{table_name}/info")
async def get_table_fields(table_name: str, database_id: int) -> Dict:
    engine = await get_cached_async_engine(database_id=database_id)
    async with engine.connect() as conn:
        dialect_name = engine.dialect.name.lower()
        columns = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_columns(table_name)
        )
        if dialect_name != "sqlite":
            table_options = await conn.run_sync(
                lambda sync_conn: inspect(sync_conn).get_table_options(
                    table_name
                )
            )
        else:
            table_options = {}
        indexes = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_indexes(table_name)
        )
    indexed_columns = set()
    for index in indexes:
        for col in index["column_names"]:
            indexed_columns.add(col)
            break
    fields = []
    for column in columns:
        fields.append(
            {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "indexed": column["name"] in indexed_columns,
                "comment": column.get("comment", column["name"]),
            }
        )
    all_indexes = []
    for index in indexes:
        unique = index.get("unique", False)
        if unique == 0:
            unique = False
        elif unique == 1:
            unique = True
        all_indexes.append(
            {
                "name": index["name"],
                "column_names": index["column_names"],
                "unique": unique,
            }
        )
    return result.success(
        {
            "table": table_name,
            "fields": fields,
            "table_options": table_options,
            "indexes": all_indexes,
        }
    )
