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
"""Database REST API"""

from typing import Annotated

from fastapi import APIRouter, Query

from src.main.app.core.schema import ListResult
from src.main.app.mapper.codegen.database_mapper import databaseMapper
from src.main.app.schema.codegen.database_schema import ListDatabasesRequest, Database
from src.main.app.service.codegen.database_service import DatabaseService
from src.main.app.service.impl.codegen.database_service_impl import DatabaseServiceImpl

database_router = APIRouter()
database_service: DatabaseService = DatabaseServiceImpl(mapper=databaseMapper)


@database_router.get("/databases")
async def list_databases(
    req: Annotated[ListDatabasesRequest, Query()],
) -> ListResult[Database]:
    """
    List databases with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResult: Paginated list of databases and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    database_records, total = await database_service.list_databases(req=req)

    return ListResult(records=database_records, total=total)


#
#
# @database_router.post("/database/create")
# async def add_database(database_add: CreateDatabase) -> HttpResponse[int]:
#     """
#     Database add.
#
#     Args:
#         database_add: Data required for add.
#
#     Returns:
#         BaseResponse with new database's ID.
#     """
#     record = DatabaseModel(**database_add.model_dump())
#     database: DatabaseModel = await database_service.add(data=record)
#     return HttpResponse(data=database.id)
#
#
# @database_router.get("/database/databases")
# async def list_databases(
#     database_query: Annotated[DatabaseQuery, Query()],
# ) -> HttpResponse[ListResult]:
#     """
#     Filter databases with pagination.
#
#     Args:
#         database_query: Pagination and filter info to query
#
#     Returns:
#         BaseResponse with list and total count.
#     """
#     databases, total_count = await database_service.list_databases(
#         data=database_query
#     )
#
#     return HttpResponse(
#         data=ListResult(records=databases, total_count=total_count)
#     )
#
#
# @database_router.get("/database/version")
# async def get_database_version(database_id: Optional[int] = None) -> Dict:
#     engine = await get_cached_async_engine(database_id=database_id)
#     async with engine.connect() as conn:
#         dialect_name = engine.dialect.name.lower()
#         if dialect_name == "sqlite":
#             version_info = await conn.execute(text("SELECT sqlite_version();"))
#         elif dialect_name in ("mysql", "mariadb"):
#             version_info = await conn.execute(text("SELECT VERSION();"))
#         elif dialect_name == "postgresql":
#             version_info = await conn.execute(text("SELECT version();"))
#         else:
#             raise
#         version = str((version_info.fetchone())[0]).split("-")[0]
#     return result.success({"version_schema": f"{dialect_name}:{version}"})
#
#
# @database_router.get("/database/{database_id}/{table_name}/info")
# async def get_table_fields(table_name: str, database_id: int) -> Dict:
#     engine = await get_cached_async_engine(database_id=database_id)
#     async with engine.connect() as conn:
#         dialect_name = engine.dialect.name.lower()
#         columns = await conn.run_sync(
#             lambda sync_conn: inspect(sync_conn).get_columns(table_name)
#         )
#         if dialect_name != "sqlite":
#             table_options = await conn.run_sync(
#                 lambda sync_conn: inspect(sync_conn).get_table_options(
#                     table_name
#                 )
#             )
#         else:
#             table_options = {}
#         indexes = await conn.run_sync(
#             lambda sync_conn: inspect(sync_conn).get_indexes(table_name)
#         )
#     indexed_columns = set()
#     for index in indexes:
#         for col in index["column_names"]:
#             indexed_columns.add(col)
#             break
#     fields = []
#     for column in columns:
#         fields.append(
#             {
#                 "name": column["name"],
#                 "type": str(column["type"]),
#                 "nullable": column["nullable"],
#                 "indexed": column["name"] in indexed_columns,
#                 "comment": column.get("comment", column["name"]),
#             }
#         )
#     all_indexes = []
#     for index in indexes:
#         unique = index.get("unique", False)
#         if unique == 0:
#             unique = False
#         elif unique == 1:
#             unique = True
#         all_indexes.append(
#             {
#                 "name": index["name"],
#                 "column_names": index["column_names"],
#                 "unique": unique,
#             }
#         )
#     return result.success(
#         {
#             "table": table_name,
#             "fields": fields,
#             "table_options": table_options,
#             "indexes": all_indexes,
#         }
#     )
