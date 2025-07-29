"""Connection operation controller"""
from typing import Annotated

from fastapi import APIRouter, Query

from src.main.app.core.schema import PageResult
from src.main.app.mapper.codegen.connection_mapper import connectionMapper
from src.main.app.schema.codegen.connection_schema import ListConnectionsRequest, Connection
from src.main.app.service.codegen.connection_service import ConnectionService
from src.main.app.service.impl.codegen.connection_service_impl import ConnectionServiceImpl

connection_router = APIRouter()
connection_service: ConnectionService = ConnectionServiceImpl(
    mapper=connectionMapper
)


@connection_router.get("/connections")
async def list_connections(
    req: Annotated[ListConnectionsRequest, Query()],
) -> PageResult[Connection]:
    """
    List connections with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        PageResult: Paginated list of connections and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    connection_records, total = await connection_service.list_connections(req=req)

    return PageResult(records=connection_records, total=total)


#
#
# @connection_router.post("/connection/create")
# async def add_connection(
#     connection_add: ConnectionAdd,
# ) -> HttpResponse[int]:
#     """
#     Connection add.
#
#     Args:
#         connection_add: Data required for add.
#
#     Returns:
#         BaseResponse with new connection's ID.
#     """
#     connection: ConnectionModel = await connection_service.save(
#         data=ConnectionModel(**connection_add.model_dump())
#     )
#     return HttpResponse(data=connection.id)
#
#
# @connection_router.get("/connection/connections")
# async def list_connections(
#     connection_query: Annotated[ConnectionQuery, Query()],
# ) -> HttpResponse[PageResult]:
#     """
#     Filter connections with pagination.
#
#     Args:
#         connection_query: Pagination and filter info to query
#
#     Returns:
#         BaseResponse with list and total count.
#     """
#     records, total_count = await connection_service.list_connections(
#         data=connection_query
#     )
#     return HttpResponse(
#         data=PageResult(records=records, total_count=total_count)
#     )
#
#
# @connection_router.get("/connection/query/{connection_id}")
# async def query_connections(
#     connection_id: int,
# ) -> HttpResponse[ConnectionQueryResponse]:
#     record = await connection_service.retrieve_by_id(id=connection_id)
#     if record is None:
#         return HttpResponse(data=record)
#     return HttpResponse(data=ConnectionQueryResponse(**record.model_dump()))
#
#
# @connection_router.post("/connection/recover")
# async def recover(
#     data: ConnectionModel,
# ) -> Dict:
#     """
#     Connection recover that be deleted.
#
#     Args:
#         data: Connection recover data
#
#     Returns:
#         BaseResponse with connection's ID.
#     """
#     connection: ConnectionModel = await connection_service.save(data=data)
#     return result.success(data=connection.id)
#
#
# @connection_router.get("/connection/exporttemplate")
# async def export_template() -> StreamingResponse:
#     """
#     Export a template for connection information.
#
#     Returns:
#         StreamingResponse with connection field
#     """
#     return await export_excel(
#         schema=ConnectionExport, file_name="connection_import_template"
#     )
#
#
# @connection_router.post("/connection/import")
# async def import_connection(
#     file: UploadFile = Form(),
# ) -> Dict:
#     """
#     Import connection information from a file.
#
#     Args:
#         file: The file containing connection information to import.
#
#     Returns:
#         Success result message
#     """
#     success_count = await connection_service.import_connection(file=file)
#     return result.success(data=f"Success import count: {success_count}")
#
#
# @connection_router.get("/connection/export")
# async def export(
#     data: Annotated[ConnectionQueryForm, Query()],
# ) -> StreamingResponse:
#     """
#     Export connection information based on provided parameters.
#
#     Args:
#         data: Filtering and format parameters for export.
#
#     Returns:
#         StreamingResponse with connection info
#     """
#     return await connection_service.export_connection(params=data)
#
#
# @connection_router.put("/connection/modify")
# async def modify(
#     data: ConnectionModify,
# ) -> Dict:
#     """
#     Update connection information.
#
#     Args:
#         data: Command containing updated connection info.
#
#     Returns:
#         Success result message
#     """
#     await connection_service.modify_by_id(
#         data=ConnectionModel(**data.model_dump(exclude_unset=True))
#     )
#     return result.success()
#
#
# @connection_router.put("/connection/batchmodify")
# async def batch_modify(ids: Ids, data: ConnectionModify) -> Dict:
#     cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
#     if len(cleaned_data) == 0:
#         return result.fail("Please fill in the modify information")
#
#     await connection_service.batch_modify_by_ids(ids=ids.ids, data=cleaned_data)
#     return result.success()
#
#
# @connection_router.delete("/connection/remove/{id}")
# async def remove(
#     id: int,
# ) -> Dict:
#     """
#     Remove a connection by their ID.
#
#     Args:
#         id: Connection ID to remove.
#
#     Returns:
#         Success result message
#     """
#     await connection_service.remove_by_id(id=id)
#     return result.success()
#
#
# @connection_router.delete("/connection/batchremove")
# async def batch_remove(
#     ids: List[int] = Query(...),
# ) -> Dict:
#     """
#     Delete connections by a list of IDs.
#
#     Args:
#         ids: List of connection IDs to delete.
#
#     Returns:
#         Success result message
#     """
#     await connection_service.batch_remove_by_ids(ids=ids)
#     return result.success()
