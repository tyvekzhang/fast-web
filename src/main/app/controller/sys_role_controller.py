"""Role REST Controller"""

from typing import Annotated, List

from fastapi import APIRouter, Query, UploadFile, Form, Depends
from starlette.responses import StreamingResponse

from src.main.app.core.schema import HttpResponse, CurrentUser
from src.main.app.core.schema import PageResult
from src.main.app.core.security import get_current_user
from src.main.app.core.utils import excel_util
from src.main.app.mapper.sys_role_mapper import roleMapper
from src.main.app.model.sys_role_model import RoleModel
from src.main.app.schema.sys_role_schema import (
    RoleQuery,
    RoleModify,
    RoleCreate,
    RoleBatchModify,
    RoleDetail,
)
from src.main.app.service.impl.sys_role_service_impl import RoleServiceImpl
from src.main.app.service.sys_role_service import RoleService

role_router = APIRouter()
role_service: RoleService = RoleServiceImpl(mapper=roleMapper)


@role_router.get("/page")
async def get_role_by_page(
    role_query: Annotated[RoleQuery, Query()],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[PageResult]:
    role_page_result: PageResult = await role_service.get_role_by_page(
        role_query=role_query, current_user=current_user
    )
    return HttpResponse.success(role_page_result)


@role_router.get("/detail/{id}")
async def get_role_detail(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse[RoleDetail]:
    role_detail: RoleDetail = await role_service.get_role_detail(
        id=id, current_user=current_user
    )
    return HttpResponse.success(role_detail)


@role_router.get("/export-template")
async def export_template(
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await excel_util.export_excel(
        schema=RoleCreate, file_name="role_import_tpl"
    )


@role_router.get("/export")
async def export_role_page(
    ids: list[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await role_service.export_role_page(
        ids=ids, current_user=current_user
    )


@role_router.post("/create")
async def create_role(
    role_create: RoleCreate,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[int]:
    role: RoleModel = await role_service.create_role(
        role_create=role_create, current_user=current_user
    )
    return HttpResponse.success(role.id)


@role_router.post("/batch-create")
async def batch_create_role(
    role_create_list: List[RoleCreate],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[int]]:
    ids: List[int] = await role_service.batch_create_role(
        role_create_list=role_create_list, current_user=current_user
    )
    return HttpResponse.success(ids)


@role_router.post("/import")
async def import_role(
    file: UploadFile = Form(),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[RoleCreate]]:
    role_create_list: List[RoleCreate] = await role_service.import_role(
        file=file, current_user=current_user
    )
    return HttpResponse.success(role_create_list)


@role_router.delete("/remove/{id}")
async def remove_role(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse:
    await role_service.remove_by_id(id=id)
    return HttpResponse.success()


@role_router.delete("/batch-remove")
async def batch_remove_role(
    ids: List[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await role_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()


@role_router.put("/modify")
async def modify_role(
    role_modify: RoleModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await role_service.modify_by_id(
        data=RoleModel(**role_modify.model_dump(exclude_unset=True))
    )
    return HttpResponse.success()


@role_router.put("/batch-modify")
async def batch_modify_role(
    role_batch_modify: RoleBatchModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    cleaned_data = {
        k: v
        for k, v in role_batch_modify.model_dump().items()
        if v is not None and k != "ids"
    }
    await role_service.batch_modify_by_ids(
        ids=role_batch_modify.ids, data=cleaned_data
    )
    return HttpResponse.success()
