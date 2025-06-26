# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
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
"""DictType REST Controller"""

from typing import Annotated, List
from fastapi import APIRouter, Query, UploadFile, Form, Depends
from starlette.responses import StreamingResponse
from src.main.app.core.security import get_current_user
from src.main.app.core.schema import HttpResponse, CurrentUser
from src.main.app.core.utils import excel_util
from src.main.app.mapper.sys_dict_type_mapper import dictTypeMapper
from src.main.app.model.sys_dict_type_model import DictTypeModel
from src.main.app.core.schema import PageResult
from src.main.app.schema.sys_dict_type_schema import (
    DictTypeQuery,
    DictTypeModify,
    DictTypeCreate,
    DictTypeBatchModify,
    DictTypeDetail,
)
from src.main.app.service.impl.sys_dict_type_service_impl import (
    DictTypeServiceImpl,
)
from src.main.app.service.sys_dict_type_service import DictTypeService

dict_type_router = APIRouter()
dict_type_service: DictTypeService = DictTypeServiceImpl(mapper=dictTypeMapper)


@dict_type_router.get("/page")
async def get_dict_type_by_page(
    dict_type_query: Annotated[DictTypeQuery, Query()],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[PageResult]:
    dict_type_page_result: PageResult = (
        await dict_type_service.get_dict_type_by_page(
            dict_type_query=dict_type_query, current_user=current_user
        )
    )
    return HttpResponse.success(dict_type_page_result)


@dict_type_router.get("/detail/{id}")
async def get_dict_type_detail(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse[DictTypeDetail]:
    dict_type_detail: DictTypeDetail = (
        await dict_type_service.get_dict_type_detail(
            id=id, current_user=current_user
        )
    )
    return HttpResponse.success(dict_type_detail)


@dict_type_router.get("/export-template")
async def export_template(
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await excel_util.export_excel(
        schema=DictTypeCreate, file_name="dict_type_import_tpl"
    )


@dict_type_router.get("/export")
async def export_dict_type_page(
    ids: list[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await dict_type_service.export_dict_type_page(
        ids=ids, current_user=current_user
    )


@dict_type_router.post("/create")
async def create_dict_type(
    dict_type_create: DictTypeCreate,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[int]:
    dict_type: DictTypeModel = await dict_type_service.create_dict_type(
        dict_type_create=dict_type_create, current_user=current_user
    )
    return HttpResponse.success(dict_type.id)


@dict_type_router.post("/batch-create")
async def batch_create_dict_type(
    dict_type_create_list: List[DictTypeCreate],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[int]]:
    ids: List[int] = await dict_type_service.batch_create_dict_type(
        dict_type_create_list=dict_type_create_list, current_user=current_user
    )
    return HttpResponse.success(ids)


@dict_type_router.post("/import")
async def import_dict_type(
    file: UploadFile = Form(),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[DictTypeCreate]]:
    dict_type_create_list: List[
        DictTypeCreate
    ] = await dict_type_service.import_dict_type(
        file=file, current_user=current_user
    )
    return HttpResponse.success(dict_type_create_list)


@dict_type_router.delete("/remove/{id}")
async def remove_dict_type(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse:
    await dict_type_service.remove_by_id(id=id)
    return HttpResponse.success()


@dict_type_router.delete("/batch-remove")
async def batch_remove_dict_type(
    ids: List[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await dict_type_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()


@dict_type_router.put("/modify")
async def modify_dict_type(
    dict_type_modify: DictTypeModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await dict_type_service.modify_by_id(
        data=DictTypeModel(**dict_type_modify.model_dump(exclude_unset=True))
    )
    return HttpResponse.success()


@dict_type_router.put("/batch-modify")
async def batch_modify_dict_type(
    dict_type_batch_modify: DictTypeBatchModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    cleaned_data = {
        k: v
        for k, v in dict_type_batch_modify.model_dump().items()
        if v is not None and k != "ids"
    }
    await dict_type_service.batch_modify_by_ids(
        ids=dict_type_batch_modify.ids, data=cleaned_data
    )
    return HttpResponse.success()
