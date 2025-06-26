"""Menu REST Controller"""

from typing import Annotated, List
from fastapi import APIRouter, Query, UploadFile, Form, Depends
from starlette.responses import StreamingResponse
from src.main.app.core.security import get_current_user
from src.main.app.core.schema import HttpResponse, CurrentUser
from src.main.app.core.utils import excel_util
from src.main.app.mapper.sys_menu_mapper import menuMapper
from src.main.app.model.sys_menu_model import MenuModel
from src.main.app.core.schema import PageResult
from src.main.app.schema.sys_menu_schema import (
    MenuQuery,
    MenuModify,
    MenuCreate,
    MenuBatchModify,
    MenuDetail,
)
from src.main.app.service.impl.sys_menu_service_impl import MenuServiceImpl
from src.main.app.service.sys_menu_service import MenuService

menu_router = APIRouter()
menu_service: MenuService = MenuServiceImpl(mapper=menuMapper)


@menu_router.get("/page")
async def get_menu_by_page(
    menu_query: Annotated[MenuQuery, Query()],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[PageResult]:
    menu_page_result: PageResult = await menu_service.get_menu_by_page(
        menu_query=menu_query, current_user=current_user
    )
    return HttpResponse.success(menu_page_result)


@menu_router.get("/detail/{id}")
async def get_menu_detail(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse[MenuDetail]:
    menu_detail: MenuDetail = await menu_service.get_menu_detail(
        id=id, current_user=current_user
    )
    return HttpResponse.success(menu_detail)


@menu_router.get("/export-template")
async def export_template(
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await excel_util.export_excel(
        schema=MenuCreate, file_name="menu_import_tpl"
    )


@menu_router.get("/export")
async def export_menu_page(
    ids: list[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> StreamingResponse:
    return await menu_service.export_menu_page(
        ids=ids, current_user=current_user
    )


@menu_router.post("/create")
async def create_menu(
    menu_create: MenuCreate,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[int]:
    menu: MenuModel = await menu_service.create_menu(
        menu_create=menu_create, current_user=current_user
    )
    return HttpResponse.success(menu.id)


@menu_router.post("/batch-create")
async def batch_create_menu(
    menu_create_list: List[MenuCreate],
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[int]]:
    ids: List[int] = await menu_service.batch_create_menu(
        menu_create_list=menu_create_list, current_user=current_user
    )
    return HttpResponse.success(ids)


@menu_router.post("/import")
async def import_menu(
    file: UploadFile = Form(),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[List[MenuCreate]]:
    menu_create_list: List[MenuCreate] = await menu_service.import_menu(
        file=file, current_user=current_user
    )
    return HttpResponse.success(menu_create_list)


@menu_router.delete("/remove/{id}")
async def remove_menu(
    id: int, current_user: CurrentUser = Depends(get_current_user())
) -> HttpResponse:
    await menu_service.remove_by_id(id=id)
    return HttpResponse.success()


@menu_router.delete("/batch-remove")
async def batch_remove_menu(
    ids: List[int] = Query(...),
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await menu_service.batch_remove_by_ids(ids=ids)
    return HttpResponse.success()


@menu_router.put("/modify")
async def modify_menu(
    menu_modify: MenuModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    await menu_service.modify_by_id(
        data=MenuModel(**menu_modify.model_dump(exclude_unset=True))
    )
    return HttpResponse.success()


@menu_router.put("/batch-modify")
async def batch_modify_menu(
    menu_batch_modify: MenuBatchModify,
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse:
    cleaned_data = {
        k: v
        for k, v in menu_batch_modify.model_dump().items()
        if v is not None and k != "ids"
    }
    await menu_service.batch_modify_by_ids(
        ids=menu_batch_modify.ids, data=cleaned_data
    )
    return HttpResponse.success()
