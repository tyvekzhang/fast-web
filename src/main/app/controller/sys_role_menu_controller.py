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
"""RoleMenu REST Controller"""

from typing import Annotated, List
from fastapi import APIRouter, Query, UploadFile, Form, Depends
from starlette.responses import StreamingResponse
from src.main.app.core.security import get_current_user
from src.main.app.core.schema import HttpResponse, CurrentUser
from src.main.app.core.utils import excel_util
from src.main.app.mapper.sys_role_menu_mapper import roleMenuMapper
from src.main.app.model.sys_role_menu_model import RoleMenuModel
from src.main.app.core.schema import PageResult
from src.main.app.schema.sys_role_menu_schema import (
    RoleMenuQuery,
    RoleMenuModify,
    RoleMenuCreate,
    RoleMenuBatchModify,
    RoleMenuDetail,
)
from src.main.app.service.impl.sys_role_menu_service_impl import (
    RoleMenuServiceImpl,
)
from src.main.app.service.sys_role_menu_service import RoleMenuService

role_menu_router = APIRouter()
role_menu_service: RoleMenuService = RoleMenuServiceImpl(mapper=roleMenuMapper)


@role_menu_router.get("/page")
async def get_role_menu_by_page(
    role_menu_query: Annotated[RoleMenuQuery, Query()],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[PageResult]:
    role_menu_page_result: PageResult = (
        await role_menu_service.get_role_menu_by_page(
            role_menu_query=role_menu_query, current_user=current_user
        )
    )
    return HttpResponse.success(role_menu_page_result)


@role_menu_router.get("/detail/{id}")
async def get_role_menu_detail(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse[RoleMenuDetail]:
    role_menu_detail: RoleMenuDetail = (
        await role_menu_service.get_role_menu_detail(
            id=id, current_user=current_user
        )
    )
    return HttpResponse.success(role_menu_detail)


@role_menu_router.get("/export-template")
async def export_template(
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await excel_util.export_excel(
        schema=RoleMenuCreate, file_name="role_menu_import_tpl"
    )


@role_menu_router.get("/export")
async def export_role_menu_page(
    ids: list[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await role_menu_service.export_role_menu_page(
        ids=ids, current_user=current_user
    )


@role_menu_router.post("/create")
async def create_role_menu(
    role_menu_create: RoleMenuCreate,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[int]:
    role_menu: RoleMenuModel = await role_menu_service.create_role_menu(
        role_menu_create=role_menu_create, current_user=current_user
    )
    return HttpResponse.success(role_menu.id)


@role_menu_router.post("/batch-create")
async def batch_create_role_menu(
    role_menu_create_list: List[RoleMenuCreate],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[int]]:
    ids: List[int] = await role_menu_service.batch_create_role_menu(
        role_menu_create_list=role_menu_create_list, current_user=current_user
    )
    return HttpResponse.success(ids)


@role_menu_router.post("/import")
async def import_role_menu(
    file: UploadFile = Form(),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[RoleMenuCreate]]:
    role_menu_create_list: List[
        RoleMenuCreate
    ] = await role_menu_service.import_role_menu(
        file=file, current_user=current_user
    )
    return HttpResponse.success(role_menu_create_list)


@role_menu_router.delete("/remove/{id}")
async def remove_role_menu(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse:
    await role_menu_service.remove_by_id(id=id)
    return HttpResponse.success()


@role_menu_router.delete("/batch-remove")
async def batch_remove_role_menu(
    ids: List[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await role_menu_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()


@role_menu_router.put("/modify")
async def modify_role_menu(
    role_menu_modify: RoleMenuModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await role_menu_service.modify_by_id(
        data=RoleMenuModel(**role_menu_modify.model_dump(exclude_unset=True))
    )
    return HttpResponse.success()


@role_menu_router.put("/batch-modify")
async def batch_modify_role_menu(
    role_menu_batch_modify: RoleMenuBatchModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    cleaned_data = {
        k: v
        for k, v in role_menu_batch_modify.model_dump().items()
        if v is not None and k != "ids"
    }
    await role_menu_service.batch_modify_by_ids(
        ids=role_menu_batch_modify.ids, data=cleaned_data
    )
    return HttpResponse.success()
