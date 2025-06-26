"""UserRole REST Controller"""

from typing import Annotated, List
from fastapi import APIRouter, Query, UploadFile, Form, Depends
from starlette.responses import StreamingResponse
from src.main.app.core.security import get_current_user
from src.main.app.core.schema import HttpResponse, CurrentUser
from src.main.app.core.utils import excel_util
from src.main.app.mapper.sys_user_role_mapper import userRoleMapper
from src.main.app.model.sys_user_role_model import UserRoleModel
from src.main.app.core.schema import PageResult
from src.main.app.schema.sys_user_role_schema import (
    UserRoleQuery,
    UserRoleModify,
    UserRoleCreate,
    UserRoleBatchModify,
    UserRoleDetail,
)
from src.main.app.service.impl.sys_user_role_service_impl import (
    UserRoleServiceImpl,
)
from src.main.app.service.sys_user_role_service import UserRoleService

user_role_router = APIRouter()
user_role_service: UserRoleService = UserRoleServiceImpl(mapper=userRoleMapper)


@user_role_router.get("/page")
async def get_user_role_by_page(
    user_role_query: Annotated[UserRoleQuery, Query()],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[PageResult]:
    user_role_page_result: PageResult = (
        await user_role_service.get_user_role_by_page(
            user_role_query=user_role_query, current_user=current_user
        )
    )
    return HttpResponse.success(user_role_page_result)


@user_role_router.get("/detail/{id}")
async def get_user_role_detail(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse[UserRoleDetail]:
    user_role_detail: UserRoleDetail = (
        await user_role_service.get_user_role_detail(
            id=id, current_user=current_user
        )
    )
    return HttpResponse.success(user_role_detail)


@user_role_router.get("/export-template")
async def export_template(
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await excel_util.export_excel(
        schema=UserRoleCreate, file_name="user_role_import_tpl"
    )


@user_role_router.get("/export")
async def export_user_role_page(
    ids: list[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await user_role_service.export_user_role_page(
        ids=ids, current_user=current_user
    )


@user_role_router.post("/create")
async def create_user_role(
    user_role_create: UserRoleCreate,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[int]:
    user_role: UserRoleModel = await user_role_service.create_user_role(
        user_role_create=user_role_create, current_user=current_user
    )
    return HttpResponse.success(user_role.id)


@user_role_router.post("/batch-create")
async def batch_create_user_role(
    user_role_create_list: List[UserRoleCreate],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[int]]:
    ids: List[int] = await user_role_service.batch_create_user_role(
        user_role_create_list=user_role_create_list, current_user=current_user
    )
    return HttpResponse.success(ids)


@user_role_router.post("/import")
async def import_user_role(
    file: UploadFile = Form(),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[UserRoleCreate]]:
    user_role_create_list: List[
        UserRoleCreate
    ] = await user_role_service.import_user_role(
        file=file, current_user=current_user
    )
    return HttpResponse.success(user_role_create_list)


@user_role_router.delete("/remove/{id}")
async def remove_user_role(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse:
    await user_role_service.remove_by_id(id=id)
    return HttpResponse.success()


@user_role_router.delete("/batch-remove")
async def batch_remove_user_role(
    ids: List[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await user_role_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()


@user_role_router.put("/modify")
async def modify_user_role(
    user_role_modify: UserRoleModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await user_role_service.modify_by_id(
        data=UserRoleModel(**user_role_modify.model_dump(exclude_unset=True))
    )
    return HttpResponse.success()


@user_role_router.put("/batch-modify")
async def batch_modify_user_role(
    user_role_batch_modify: UserRoleBatchModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    cleaned_data = {
        k: v
        for k, v in user_role_batch_modify.model_dump().items()
        if v is not None and k != "ids"
    }
    await user_role_service.batch_modify_by_ids(
        ids=user_role_batch_modify.ids, data=cleaned_data
    )
    return HttpResponse.success()
