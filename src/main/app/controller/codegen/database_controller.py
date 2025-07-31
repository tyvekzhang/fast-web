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
