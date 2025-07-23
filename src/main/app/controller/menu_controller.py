"""Menu REST Controller"""

from typing import Annotated

from fastapi import APIRouter, Query, Form
from starlette.responses import StreamingResponse

from src.main.app.core.schema import PageResult
from src.main.app.mapper.menu_mapper import menuMapper
from src.main.app.model.menu_model import MenuModel
from src.main.app.schema.menu_schema import (
    ListMenusRequest,
    Menu,
    CreateMenuRequest,
    MenuDetail,
    UpdateMenuRequest,
    BatchDeleteMenusRequest,
    BatchUpdateMenusRequest,
    BatchUpdateMenusResponse,
    BatchCreateMenusRequest,
    BatchCreateMenuResponse,
    ExportMenusRequest,
    ImportMenusResponse,
    BatchGetMenusResponse,
    ImportMenusRequest,
    ImportMenu,
    BatchPatchMenusRequest,
)
from src.main.app.service.impl.menu_service_impl import MenuServiceImpl
from src.main.app.service.menu_service import MenuService

menu_router = APIRouter()
menu_service: MenuService = MenuServiceImpl(mapper=menuMapper)


@menu_router.get("/menus/{id}")
async def get_menu(id: int) -> MenuDetail:
    """
    Retrieve menu details.

    Args:

        id: Unique ID of the menu resource.

    Returns:

        MenuDetail: The menu object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested menu does not exist.
    """
    menu_record: MenuModel = await menu_service.get_menu(id=id)
    return MenuDetail(**menu_record.model_dump())


@menu_router.get("/menus")
async def list_menus(
    req: Annotated[ListMenusRequest, Query()],
) -> PageResult[Menu]:
    """
    List menus with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        PageResult: Paginated list of menus and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    menu_records, total = await menu_service.list_menus(req=req)
    menu_records_with_children: list[
        Menu
    ] = await menu_service.get_children_recursively(
        parent_data=menu_records, schema_class=Menu
    )
    return PageResult(records=menu_records_with_children, total=total)


@menu_router.post("/menus")
async def creat_menu(
    req: CreateMenuRequest,
) -> Menu:
    """
    Create a new menu.

    Args:

        req: Request object containing menu creation data.

    Returns:

         Menu: The menu object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    menu: MenuModel = await menu_service.create_menu(req=req)
    return Menu(**menu.model_dump())


@menu_router.put("/menus")
async def update_menu(
    req: UpdateMenuRequest,
) -> Menu:
    """
    Update an existing menu.

    Args:

        req: Request object containing menu update data.

    Returns:

        Menu: The updated menu object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the menu to update doesn't exist.
    """
    menu: MenuModel = await menu_service.update_menu(req=req)
    return Menu(**menu.model_dump())


@menu_router.delete("/menus/{id}")
async def delete_menu(
    id: int,
) -> None:
    """
    Delete menu by ID.

    Args:

        id: The ID of the menu to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the menu with given ID doesn't exist.
    """
    await menu_service.delete_menu(id=id)


@menu_router.get("/menus:batchGet")
async def batch_get_menus(
    ids: list[int] = Query(..., description="List of menu IDs to retrieve"),
) -> BatchGetMenusResponse:
    """
    Retrieves multiple menus by their IDs.

    Args:

        ids (list[int]): A list of menu resource IDs.

    Returns:

        list[MenuDetail]: A list of menu objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested menus does not exist.
    """
    menu_records: list[MenuModel] = await menu_service.batch_get_menus(ids)
    menu_detail_list: list[MenuDetail] = [
        MenuDetail(**menu_record.model_dump()) for menu_record in menu_records
    ]
    return BatchGetMenusResponse(menus=menu_detail_list)


@menu_router.post("/menus:batchCreate")
async def batch_create_menus(
    req: BatchCreateMenusRequest,
) -> BatchCreateMenuResponse:
    """
    Batch create menus.

    Args:

        req (BatchCreateMenusRequest): Request body containing a list of menu creation items.

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


@menu_router.post("/menus:batchUpdate")
async def batch_update_menus(
    req: BatchUpdateMenusRequest,
) -> BatchUpdateMenusResponse:
    """
    Batch update multiple menus with the same changes.

    Args:

        req (BatchUpdateMenusRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated menus.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify menus
        HTTPException 404 (Not Found): If any specified menu ID doesn't exist
    """
    menu_records: list[MenuModel] = await menu_service.batch_update_menus(
        req=req
    )
    menu_list: list[Menu] = [Menu(**menu.model_dump()) for menu in menu_records]
    return BatchUpdateMenusResponse(menus=menu_list)


@menu_router.post("/menus:batchPatch")
async def batch_patch_menus(
    req: BatchPatchMenusRequest,
) -> BatchUpdateMenusResponse:
    """
    Batch update multiple menus with individual changes.

    Args:

        req (BatchPatchMenusRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated menus.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify menus
        HTTPException 404 (Not Found): If any specified menu ID doesn't exist
    """
    menu_records: list[MenuModel] = await menu_service.batch_patch_menus(
        req=req
    )
    menu_list: list[Menu] = [Menu(**menu.model_dump()) for menu in menu_records]
    return BatchUpdateMenusResponse(menus=menu_list)


@menu_router.post("/menus:batchDelete")
async def batch_delete_menus(
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
    await menu_service.batch_delete_menus(req=req)


@menu_router.get("/menus:exportTemplate")
async def export_menus_template() -> StreamingResponse:
    """
    Export the Excel template for menu import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await menu_service.export_menus_template()


@menu_router.get("/menus:export")
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
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching menus are found.
    """
    return await menu_service.export_menus(
        req=req,
    )


@menu_router.post("/menus:import")
async def import_menus(
    req: ImportMenusRequest = Form(...),
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

    import_menus_resp: list[ImportMenu] = await menu_service.import_menus(
        req=req
    )
    return ImportMenusResponse(menus=import_menus_resp)
