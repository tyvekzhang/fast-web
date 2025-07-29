# """GenTableColumn operation controller"""
#
# from typing import Dict, Annotated, List
#
# from fastapi import APIRouter, Query, UploadFile, Form
# from src.main.app.core import result
# from src.main.app.core.result import HttpResponse
# from src.main.app.core.utils.excel_util import export_excel
# from src.main.app.mapper.gen_field_mapper import genFieldMapper
# from src.main.app.model.gen_field_model import GenFieldModel
# from src.main.app.schema.common_schema import PageResult
# from src.main.app.schema.gen_field_schema import (
#     GenTableColumnAdd,
#     GenTableColumnExport,
#     GenTableColumnQueryForm,
#     GenTableColumnModify,
#     GenTableColumnQuery,
# )
# from src.main.app.schema.user_schema import Ids
# from src.main.app.service.gen_table_field_service import GenTableFieldService
# from src.main.app.service.impl.gen_table_field_service_impl import (
#     GenTableFieldServiceImpl,
# )
# from starlette.responses import StreamingResponse
#
# gen_field_router = APIRouter()
# gen_table_column_service: GenTableFieldService = GenTableFieldServiceImpl(
#     mapper=genFieldMapper
# )
#
#
# @gen_field_router.post("/gen-field/add")
# async def add_gen_table_column(
#     gen_table_column_add: GenTableColumnAdd,
# ) -> HttpResponse[int]:
#     """
#     GenTableColumn add.
#
#     Args:
#         gen_table_column_add: Data required for add.
#
#     Returns:
#         BaseResponse with new gen_table_column's ID.
#     """
#     gen_table_column: GenFieldModel = await gen_table_column_service.save(
#         data=GenFieldModel(**gen_table_column_add.model_dump())
#     )
#     return HttpResponse(data=gen_table_column.id)
#
#
# @gen_field_router.get("/gen-field/gen_table_columns")
# async def list_gen_table_columns(
#     gen_table_column_query: Annotated[GenTableColumnQuery, Query()],
# ) -> HttpResponse[PageResult]:
#     """
#     Filter gen_table_columns with pagination.
#
#     Args:
#         gen_table_column_query: Pagination and filter info to query
#
#     Returns:
#         BaseResponse with list and total count.
#     """
#     (
#         records,
#         total_count,
#     ) = await gen_table_column_service.list_gen_table_columns(
#         data=gen_table_column_query
#     )
#     return HttpResponse(
#         data=PageResult(records=records, total_count=total_count)
#     )
#
#
# @gen_field_router.post("/gen-field/recover")
# async def recover(
#     data: GenFieldModel,
# ) -> Dict:
#     """
#     GenTableColumn recover that be deleted.
#
#     Args:
#         data: GenTableColumn recover data
#
#     Returns:
#         BaseResponse with gen_table_column's ID.
#     """
#     gen_table_column: GenFieldModel = await gen_table_column_service.save(
#         data=data
#     )
#     return result.success(data=gen_table_column.id)
#
#
# @gen_field_router.get("/gen-field/exporttemplate")
# async def export_template() -> StreamingResponse:
#     """
#     Export a template for gen_table_column information.
#
#     Returns:
#         StreamingResponse with gen_table_column field
#     """
#     return await export_excel(
#         schema=GenTableColumnExport,
#         file_name="gen_table_column_import_template",
#     )
#
#
# @gen_field_router.post("/gen-field/import")
# async def import_gen_table_column(
#     file: UploadFile = Form(),
# ) -> Dict:
#     """
#     Import gen_table_column information from a file.
#
#     Args:
#         file: The file containing gen_table_column information to import.
#
#     Returns:
#         Success result message
#     """
#     success_count = await gen_table_column_service.import_gen_table_column(
#         file=file
#     )
#     return result.success(data=f"Success import count: {success_count}")
#
#
# @gen_field_router.get("/gen-field/export")
# async def export(
#     data: Annotated[GenTableColumnQueryForm, Query()],
# ) -> StreamingResponse:
#     """
#     Export gen_table_column information based on provided parameters.
#
#     Args:
#         data: Filtering and format parameters for export.
#
#     Returns:
#         StreamingResponse with gen_table_column info
#     """
#     return await gen_table_column_service.export_gen_table_column(params=data)
#
#
# @gen_field_router.put("/gen-field/modify")
# async def modify(
#     data: GenTableColumnModify,
# ) -> Dict:
#     """
#     Update gen_table_column information.
#
#     Args:
#         data: Command containing updated gen_table_column info.
#
#     Returns:
#         Success result message
#     """
#     await gen_table_column_service.modify_by_id(
#         data=GenFieldModel(**data.model_dump(exclude_unset=True))
#     )
#     return result.success()
#
#
# @gen_field_router.put("/gen-field/batchmodify")
# async def batch_modify(ids: Ids, data: GenTableColumnModify) -> Dict:
#     cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
#     if len(cleaned_data) == 0:
#         return result.fail("Please fill in the modify information")
#
#     await gen_table_column_service.batch_modify_by_ids(
#         ids=ids.ids, data=cleaned_data
#     )
#     return result.success()
#
#
# @gen_field_router.delete("/gen-field/remove/{id}")
# async def remove(
#     id: int,
# ) -> Dict:
#     """
#     Remove a gen_table_column by their ID.
#
#     Args:
#         id: GenTableColumn ID to remove.
#
#     Returns:
#         Success result message
#     """
#     await gen_table_column_service.remove_by_id(id=id)
#     return result.success()
#
#
# @gen_field_router.delete("/gen-field/batchremove")
# async def batch_remove(
#     ids: List[int] = Query(...),
# ) -> Dict:
#     """
#     Delete gen_table_columns by a list of IDs.
#
#     Args:
#         ids: List of gen_table_column IDs to delete.
#
#     Returns:
#         Success result message
#     """
#     await gen_table_column_service.batch_remove_by_ids(ids=ids)
#     return result.success()
