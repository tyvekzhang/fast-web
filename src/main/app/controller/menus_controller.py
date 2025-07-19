"""Menu REST Controller"""

from typing import Annotated

from fastapi import APIRouter, Query, UploadFile, Form
from starlette.responses import StreamingResponse

from src.main.app.core.schema import PageResult
from src.main.app.mapper.menus_mapper import menuMapper
from src.main.app.model.menus_model import MenuModel
from src.main.app.schema.menus_schema import (
    ListMenuRequest,
    Menu,
    CreateMenuRequest,
    MenuDetail,
    UpdateMenuRequest,
    BatchDeleteMenusRequest,
    BatchUpdateMenusRequest,
    BatchUpdateMenusResponse,
    BatchCreateMenuRequest,
    BatchCreateMenuResponse,
    ExportMenusRequest,
    ImportMenusResponse,
    BatchGetMenusResponse,
)
from src.main.app.service.impl.menus_service_impl import MenuServiceImpl
from src.main.app.service.menus_service import MenuService

menus_router = APIRouter()
menu_service: MenuService = MenuServiceImpl(mapper=menuMapper)


@menus_router.get("/menus/{id}")
async def get_menu(id: int) -> MenuDetail:
    """
    Retrieve menu with detail data.

    Args:

        id: The resource id of the menu.

    Returns:

        MenuDetail: The menu object with detail data.

    Raises:

        HttpException(403 Forbidden): If the current user don't have access rights.
        HTTPException(404 Not Found): If the menu does not exist.
    """
    menu_record: MenuModel = await menu_service.get_menu(id=id)
    return MenuDetail(**menu_record.model_dump())


@menus_router.get("/menus")
async def list_menus(
    req: Annotated[ListMenuRequest, Query()],
) -> PageResult[Menu]:
    """
    List menus with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        PageResult: Paginated list of menus and total count

    Raises:

        HttpException(403 Forbidden): If user don't have access rights
    """
    menu_records, total = await menu_service.list_menus(req=req)
    menu_records_with_children: list[
        Menu
    ] = await menu_service.get_children_recursively(
        parent_data=menu_records, schema_class=Menu
    )
    return PageResult(records=menu_records_with_children, total=total)


@menus_router.post("/menus")
async def creat_menu(
    req: CreateMenuRequest,
) -> Menu:
    """
    Create a new menu

    Args:

        req: Request object containing menu creation data

    Returns:

         Menu: The menu object

    Raises:

        HttpException(403 Forbidden): If the current user don't have access rights.
        HttpException(409 Conflict): If the creation data already exists.
    """
    menu: MenuModel = await menu_service.create_menu(req=req)
    return Menu(**menu.model_dump())


@menus_router.put("/menus")
async def update_menu(
    req: UpdateMenuRequest,
) -> Menu:
    """
    Update an existing menu

    Args:

        req: Request object containing menu update data

    Returns:

        Menu: The updated menu object

    Raises:

        HttpException(403 Forbidden): If the current user doesn't have update permissions
        HttpException(404 Not Found): If the menu to update doesn't exist
    """
    menu: MenuModel = await menu_service.update_menu(req=req)
    return Menu(**menu.model_dump())


@menus_router.delete("/menus/{id}")
async def delete_menu(
    id: int,
) -> None:
    """
    Delete menu by ID

    Args:

        id: The ID of the menu to delete

    Raises:

        HttpException(403 Forbidden): If the current user doesn't have access permissions
        HttpException(404 Not Found): If the menu with given ID doesn't exist
    """
    await menu_service.delete_menu(id=id)


@menus_router.get("/menus:batchGet")
async def batch_get_menus(
    ids: list[int] = Query(..., description="List of menu IDs to retrieve"),
) -> BatchGetMenusResponse[list[MenuDetail]]:
    """
    Retrieves multiple menus by their IDs.

    Args:

        ids (list[int]): A list of menu resource IDs.

    Returns:

        list[MenuDetail]: A list of menu objects matching the provided IDs.

    Raises:

        HttpException(403 Forbidden): If the current user does not have access rights.
        HttpException(404 Not Found): If one of the requested menus does not exist.
    """
    menu_records: list[MenuModel] = await menu_service.batch_get_menus(ids)
    menu_detail_list: list[MenuDetail] = [
        MenuDetail(**menu_record.model_dump()) for menu_record in menu_records
    ]
    return BatchGetMenusResponse(menus=menu_detail_list)


@menus_router.post("/menus:batchCreate")
async def batch_create_menus(
    req: BatchCreateMenuRequest,
) -> BatchCreateMenuResponse:
    """
    Batch create menus.

    Args:

        req (BatchCreateMenuRequest): Request body containing a list of menu creation items.

    Returns:

        BatchCreateMenuResponse: Response containing the list of created menus.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any menu creation data already exists.
    """

    menu_records = await menu_service.batch_create_menus(req=req)
    menu_list: list[Menu] = [
        Menu(**menu_record.model_dump()) for menu_record in menu_records
    ]
    return BatchCreateMenuResponse(menus=menu_list)


@menus_router.post("/menus:batchUpdate")
async def batch_update_menus(
    req: BatchUpdateMenusRequest,
) -> BatchUpdateMenusResponse:
    """
    Batch updates multiple menus in a single operation.

    Args:

        req (BatchUpdateMenusRequest): The batch update request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated menus.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify menus
        HTTPException 404 (Not Found): If any specified menu ID doesn't exist
    """
    resp = menu_service.batch_update_menus(req=req)
    return resp


@menus_router.post("/menus:batchDelete")
async def batch_remove_menus(
    req: BatchDeleteMenusRequest,
) -> None:
    """
    Batch delete menus.

    Args:
        req (BatchDeleteMenusRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the menus do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await menu_service.batch_remove_menus(req=req)


@menus_router.post("/menus:import")
async def import_menus(
    req: UploadFile = Form(...),
) -> ImportMenusResponse:
    """
    Import menus from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing menu data to import.

    Returns:
        ImportMenusResponse: List of successfully parsed menu data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    return await menu_service.import_menus(req=req)


@menus_router.get("/menus:exportTemplate")
async def export_menus_template() -> StreamingResponse:
    """
    Export the Excel template for menu import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.
    """

    return await menu_service.export_menus_template()


@menus_router.get("/menus:export")
async def export_menus(
    req: ExportMenusRequest = Query(...),
) -> StreamingResponse:
    """
    Export menu data based on the provided menu IDs.

    Args:
        req (ExportMenusRequest): Query parameters specifying the menus to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(404): If no matching menus are found.
        HTTPException(500): If an internal error occurs during export.
    """
    return await menu_service.export_menus(
        req=req,
    )
