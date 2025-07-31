"""Connection REST API"""

from typing import Annotated

from fastapi import APIRouter, Query

from src.main.app.core.schema import ListResult
from src.main.app.mapper.codegen.connection_mapper import connectionMapper
from src.main.app.schema.codegen.connection_schema import ListConnectionsRequest, Connection
from src.main.app.service.codegen.connection_service import ConnectionService
from src.main.app.service.impl.codegen.connection_service_impl import ConnectionServiceImpl

connection_router = APIRouter()
connection_service: ConnectionService = ConnectionServiceImpl(mapper=connectionMapper)


@connection_router.get("/connections")
async def list_connections(
    req: Annotated[ListConnectionsRequest, Query()],
) -> ListResult[Connection]:
    """
    List connections with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResult: Paginated list of connections and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    connection_records, total = await connection_service.list_connections(req=req)

    return ListResult(records=connection_records, total=total)
