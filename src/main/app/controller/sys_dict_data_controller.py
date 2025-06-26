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
"""DictData REST Controller"""

from typing import Annotated, List
from fastapi import APIRouter, Query, UploadFile, Form, Depends
from starlette.responses import StreamingResponse
from src.main.app.core.security import get_current_user
from src.main.app.core.schema import HttpResponse, CurrentUser
from src.main.app.core.utils import excel_util
from src.main.app.mapper.sys_dict_data_mapper import dictDataMapper
from src.main.app.model.sys_dict_data_model import DictDataModel
from src.main.app.core.schema import PageResult
from src.main.app.schema.sys_dict_data_schema import (
    DictDataQuery,
    DictDataModify,
    DictDataCreate,
    DictDataBatchModify,
    DictDataDetail,
)
from src.main.app.service.impl.sys_dict_data_service_impl import (
    DictDataServiceImpl,
)
from src.main.app.service.sys_dict_data_service import DictDataService

dict_data_router = APIRouter()
dict_data_service: DictDataService = DictDataServiceImpl(mapper=dictDataMapper)


@dict_data_router.get("/page")
async def get_dict_data_by_page(
    dict_data_query: Annotated[DictDataQuery, Query()],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[PageResult]:
    dict_data_page_result: PageResult = (
        await dict_data_service.get_dict_data_by_page(
            dict_data_query=dict_data_query, current_user=current_user
        )
    )
    return HttpResponse.success(dict_data_page_result)


@dict_data_router.get("/detail/{id}")
async def get_dict_data_detail(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse[DictDataDetail]:
    dict_data_detail: DictDataDetail = (
        await dict_data_service.get_dict_data_detail(
            id=id, current_user=current_user
        )
    )
    return HttpResponse.success(dict_data_detail)


@dict_data_router.get("/export-template")
async def export_template(
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await excel_util.export_excel(
        schema=DictDataCreate, file_name="dict_data_import_tpl"
    )


@dict_data_router.get("/export")
async def export_dict_data_page(
    ids: list[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await dict_data_service.export_dict_data_page(
        ids=ids, current_user=current_user
    )


@dict_data_router.post("/create")
async def create_dict_data(
    dict_data_create: DictDataCreate,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[int]:
    dict_data: DictDataModel = await dict_data_service.create_dict_data(
        dict_data_create=dict_data_create, current_user=current_user
    )
    return HttpResponse.success(dict_data.id)


@dict_data_router.post("/batch-create")
async def batch_create_dict_data(
    dict_data_create_list: List[DictDataCreate],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[int]]:
    ids: List[int] = await dict_data_service.batch_create_dict_data(
        dict_data_create_list=dict_data_create_list, current_user=current_user
    )
    return HttpResponse.success(ids)


@dict_data_router.post("/import")
async def import_dict_data(
    file: UploadFile = Form(),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[DictDataCreate]]:
    dict_data_create_list: List[
        DictDataCreate
    ] = await dict_data_service.import_dict_data(
        file=file, current_user=current_user
    )
    return HttpResponse.success(dict_data_create_list)


@dict_data_router.delete("/remove/{id}")
async def remove_dict_data(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse:
    await dict_data_service.remove_by_id(id=id)
    return HttpResponse.success()


@dict_data_router.delete("/batch-remove")
async def batch_remove_dict_data(
    ids: List[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await dict_data_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()


@dict_data_router.put("/modify")
async def modify_dict_data(
    dict_data_modify: DictDataModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await dict_data_service.modify_by_id(
        data=DictDataModel(**dict_data_modify.model_dump(exclude_unset=True))
    )
    return HttpResponse.success()


@dict_data_router.put("/batch-modify")
async def batch_modify_dict_data(
    dict_data_batch_modify: DictDataBatchModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    cleaned_data = {
        k: v
        for k, v in dict_data_batch_modify.model_dump().items()
        if v is not None and k != "ids"
    }
    await dict_data_service.batch_modify_by_ids(
        ids=dict_data_batch_modify.ids, data=cleaned_data
    )
    return HttpResponse.success()
