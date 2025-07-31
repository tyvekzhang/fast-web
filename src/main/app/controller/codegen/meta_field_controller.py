# """Field operation controller"""
#
# from typing import Dict, Annotated, List
#
# from fastapi import APIRouter, Query, UploadFile, Form
# from src.main.app.core import result
# from src.main.app.core.result import HttpResponse
# from src.main.app.core.utils.excel_util import export_excel
# from src.main.app.mapper.field_mapper import fieldMapper
# from src.main.app.model.db_field_model import FieldModel
# from src.main.app.schema.common_schema import ListResult
# from src.main.app.schema.field_schema import (
#     FieldAdd,
#     FieldExport,
#     FieldQueryForm,
#     FieldModify,
#     FieldQuery,
#     AntTableColumn,
# )
# from src.main.app.schema.user_schema import Ids
# from src.main.app.service.field_service import FieldService
# from src.main.app.service.impl.field_service_impl import FieldServiceImpl
# from starlette.responses import StreamingResponse
#
# field_router = APIRouter()
# field_service: FieldService = FieldServiceImpl(mapper=fieldMapper)
#
#
# @field_router.get("/field/antd/{id}")
# async def get_ant_table_columns(id: int) -> HttpResponse[List[AntTableColumn]]:
#     gen_fields = await field_service.get_ant_table_fields(table_id=id)
#     return HttpResponse(data=gen_fields)
#
#
# @field_router.post("/field/add")
# async def add_field(
#     field_add: FieldAdd,
# ) -> HttpResponse[int]:
#     """
#     Field add.
#
#     Args:
#         field_add: Data required for add.
#
#     Returns:
#         BaseResponse with new field's ID.
#     """
#     field: FieldModel = await field_service.save(
#         data=FieldModel(**field_add.model_dump())
#     )
#     return HttpResponse(data=field.id)
#
#
# @field_router.get("/field/gen_fields")
# async def list_fields(
#     field_query: Annotated[FieldQuery, Query()],
# ) -> HttpResponse[ListResult]:
#     """
#     Filter gen_fields with pagination.
#
#     Args:
#         field_query: Pagination and filter info to query
#
#     Returns:
#         BaseResponse with list and total count.
#     """
#     records, total_count = await field_service.list_fields(data=field_query)
#     return HttpResponse(
#         data=ListResult(records=records, total_count=total_count)
#     )
#
#
# @field_router.post("/field/recover")
# async def recover(
#     data: FieldModel,
# ) -> Dict:
#     """
#     Field recover that be deleted.
#
#     Args:
#         data: Field recover data
#
#     Returns:
#         BaseResponse with field's ID.
#     """
#     field: FieldModel = await field_service.save(data=data)
#     return result.success(data=field.id)
#
#
# @field_router.get("/field/exporttemplate")
# async def export_template() -> StreamingResponse:
#     """
#     Export a template for field information.
#
#     Returns:
#         StreamingResponse with field field
#     """
#     return await export_excel(
#         schema=FieldExport, file_name="field_import_template"
#     )
#
#
# @field_router.post("/field/import")
# async def import_field(
#     file: UploadFile = Form(),
# ) -> Dict:
#     """
#     Import field information from a file.
#
#     Args:
#         file: The file containing field information to import.
#
#     Returns:
#         Success result message
#     """
#     success_count = await field_service.import_field(file=file)
#     return result.success(data=f"Success import count: {success_count}")
#
#
# @field_router.get("/field/export")
# async def export(
#     data: Annotated[FieldQueryForm, Query()],
# ) -> StreamingResponse:
#     """
#     Export field information based on provided parameters.
#
#     Args:
#         data: Filtering and format parameters for export.
#
#     Returns:
#         StreamingResponse with field info
#     """
#     return await field_service.export_field(params=data)
#
#
# @field_router.put("/field/modify")
# async def modify(
#     data: FieldModify,
# ) -> Dict:
#     """
#     Update field information.
#
#     Args:
#         data: Command containing updated field info.
#
#     Returns:
#         Success result message
#     """
#     await field_service.modify_by_id(
#         data=FieldModel(**data.model_dump(exclude_unset=True))
#     )
#     return result.success()
#
#
# @field_router.put("/field/batchmodify")
# async def batch_modify(ids: Ids, data: FieldModify) -> Dict:
#     cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
#     if len(cleaned_data) == 0:
#         return result.fail("Please fill in the modify information")
#
#     await field_service.batch_modify_by_ids(ids=ids.ids, data=cleaned_data)
#     return result.success()
#
#
# @field_router.delete("/field/remove/{id}")
# async def remove(
#     id: int,
# ) -> Dict:
#     """
#     Remove a field by their ID.
#
#     Args:
#         id: Field ID to remove.
#
#     Returns:
#         Success result message
#     """
#     await field_service.remove_by_id(id=id)
#     return result.success()
#
#
# @field_router.delete("/field/batchremove")
# async def batch_remove(
#     ids: List[int] = Query(...),
# ) -> Dict:
#     """
#     Delete gen_fields by a list of IDs.
#
#     Args:
#         ids: List of field IDs to delete.
#
#     Returns:
#         Success result message
#     """
#     await field_service.batch_remove_by_ids(ids=ids)
#     return result.success()
