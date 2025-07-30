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
#
# """Index operation controller"""
#
# import subprocess
# import sys
# from typing import Dict, Annotated, List
#
# from fastapi import APIRouter, Query, UploadFile, Form
# from src.main.app.core import result
# from src.main.app.core.result import HttpResponse
# from src.main.app.core.utils.excel_util import export_excel
# from src.main.app.mapper.index_mapper import indexMapper
# from src.main.app.model.db_index_model import IndexModel
# from src.main.app.schema.common_schema import ListResult
# from src.main.app.schema.index_schema import (
#     IndexAdd,
#     IndexExport,
#     IndexQueryForm,
#     IndexModify,
#     IndexQuery,
# )
# from src.main.app.schema.user_schema import Ids
# from src.main.app.service.index_service import IndexService
# from src.main.app.service.impl.index_service_impl import IndexServiceImpl
# from starlette.responses import StreamingResponse
#
# index_router = APIRouter()
# index_service: IndexService = IndexServiceImpl(mapper=indexMapper)
#
#
# @index_router.post("/index/add")
# async def add_index(
#     data: IndexAdd,
# ) -> Dict:
#     """
#     Index add.
#
#     Args:
#         data: Data required for add.
#
#     Returns:
#         BaseResponse with new index's ID.
#     """
#     index: IndexModel = await index_service.save(data=IndexModel(**data.model_dump()))
#     return result.success(data=index.id)
#
#
# @index_router.get("/index/indexes")
# async def list_indexes(
#     index_query: Annotated[IndexQuery, Query()],
# ) -> HttpResponse[ListResult]:
#     """
#     Filter indexes with pagination.
#
#     Args:
#         index_query: Pagination and filter info to query
#
#     Returns:
#         BaseResponse with list and total count.
#     """
#     index_list, total_count = await index_service.list_indexes(data=index_query)
#
#     return HttpResponse(
#         data=ListResult(records=index_list, total_count=total_count)
#     )
#
#
# @index_router.post("/index/run_script")
# async def run_script(script_path: str):
#     try:
#         # 使用 subprocess 执行 Python 脚本
#         result = subprocess.run(
#             [sys.execuindex, script_path],
#             capture_output=True,
#             text=True,
#             check=True,
#         )
#         return {"stdout": result.stdout, "stderr": result.stderr}
#     except subprocess.CalledProcessError as e:
#         return {"error": str(e), "stdout": e.stdout, "stderr": e.stderr}
#
#
# @index_router.post("/index/recover")
# async def recover(
#     data: IndexModel,
# ) -> Dict:
#     """
#     Index recover that be deleted.
#
#     Args:
#         data: Index recover data
#
#     Returns:
#         BaseResponse with index's ID.
#     """
#     index: IndexModel = await index_service.save(data=data)
#     return result.success(data=index.id)
#
#
# @index_router.get("/index/exporttemplate")
# async def export_template() -> StreamingResponse:
#     """
#     Export a template for index information.
#
#     Returns:
#         StreamingResponse with index field
#     """
#     return await export_excel(
#         schema=IndexExport, file_name="index_import_template"
#     )
#
#
# @index_router.post("/index/import")
# async def import_index(
#     file: UploadFile = Form(),
# ) -> Dict:
#     """
#     Import index information from a file.
#
#     Args:
#         file: The file containing index information to import.
#
#     Returns:
#         Success result message
#     """
#     success_count = await index_service.import_index(file=file)
#     return result.success(data=f"Success import count: {success_count}")
#
#
# @index_router.get("/index/export")
# async def export(
#     data: Annotated[IndexQueryForm, Query()],
# ) -> StreamingResponse:
#     """
#     Export index information based on provided parameters.
#
#     Args:
#         data: Filtering and format parameters for export.
#
#     Returns:
#         StreamingResponse with index info
#     """
#     return await index_service.export_index(params=data)
#
#
# @index_router.put("/index/modify")
# async def modify(
#     data: IndexModify,
# ) -> Dict:
#     """
#     Update index information.
#
#     Args:
#         data: Command containing updated index info.
#
#     Returns:
#         Success result message
#     """
#     await index_service.modify_by_id(
#         data=IndexModel(**data.model_dump(exclude_unset=True))
#     )
#     return result.success()
#
#
# @index_router.put("/index/batchmodify")
# async def batch_modify(ids: Ids, data: IndexModify) -> Dict:
#     cleaned_data = {k: v for k, v in data.model_dump().items() if v is not None}
#     if len(cleaned_data) == 0:
#         return result.fail("Please fill in the modify information")
#
#     await index_service.batch_modify_by_ids(ids=ids.ids, data=cleaned_data)
#     return result.success()
#
#
# @index_router.delete("/index/remove/{id}")
# async def remove(
#     id: int,
# ) -> Dict:
#     """
#     Remove a index by their ID.
#
#     Args:
#         id: Index ID to remove.
#
#     Returns:
#         Success result message
#     """
#     await index_service.remove_by_id(id=id)
#     return result.success()
#
#
# @index_router.delete("/index/batchremove")
# async def batch_remove(
#     ids: List[int] = Query(...),
# ) -> Dict:
#     """
#     Delete indexs by a list of IDs.
#
#     Args:
#         ids: List of index IDs to delete.
#
#     Returns:
#         Success result message
#     """
#     await index_service.batch_remove_by_ids(ids=ids)
#     return result.success()
