"""Menu domain service impl"""

from __future__ import annotations

import io
import json
from datetime import datetime
from typing import Optional, Type, Any
from typing import Union

import pandas as pd
from fastapi import UploadFile
from loguru import logger
from pydantic import ValidationError
from starlette.responses import StreamingResponse

from src.main.app.core.constant import FilterOperators
from src.main.app.core.schema import CurrentUser
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.core.utils import excel_util
from src.main.app.core.utils.validate_util import ValidateService
from src.main.app.enums import BusinessErrorCode
from src.main.app.exception.biz_exception import BusinessException
from src.main.app.mapper.menu_mapper import MenuMapper
from src.main.app.model.menus_model import MenuModel
from src.main.app.schema.menus_schema import (
    ListMenuRequest,
    Menu,
    CreateMenuRequest,
    UpdateMenuRequest,
    BatchDeleteMenusRequest,
    ExportMenusRequest,
    BatchCreateMenuRequest,
    CreateMenu,
    BatchUpdateMenusRequest,
    UpdateMenu,
    ImportMenusRequest,
    ImportMenu,
    ExportMenu,
)
from src.main.app.service.menus_service import MenuService


class MenuServiceImpl(BaseServiceImpl[MenuMapper, MenuModel], MenuService):
    """
    Implementation of the MenuService interface.
    """

    def __init__(self, mapper: MenuMapper):
        """
        Initialize the MenuServiceImpl instance.

        Args:
            mapper (MenuMapper): The MenuMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def get_menu(
        self,
        *,
        id: int,
    ) -> MenuModel:
        menu_record: MenuModel = await self.mapper.select_by_id(id=id)
        if menu_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return menu_record

    async def list_menus(
        self, req: ListMenuRequest
    ) -> tuple[list[MenuModel], int]:
        filters = {
            FilterOperators.EQ: {},
            FilterOperators.NE: {},
            FilterOperators.GT: {},
            FilterOperators.GE: {},
            FilterOperators.LT: {},
            FilterOperators.LE: {},
            FilterOperators.BETWEEN: {},
            FilterOperators.LIKE: {},
        }
        if req.parent_id is not None and req.parent_id != "":
            filters[FilterOperators.EQ]["parent_id"] = req.parent_id
        else:
            filters[FilterOperators.EQ]["parent_id"] = 0
        if req.id is not None and req.id != "":
            filters[FilterOperators.EQ]["id"] = req.id
        if req.name is not None and req.name != "":
            filters[FilterOperators.LIKE]["name"] = req.name
        if req.icon is not None and req.icon != "":
            filters[FilterOperators.EQ]["icon"] = req.icon
        if req.permission is not None and req.permission != "":
            filters[FilterOperators.EQ]["permission"] = req.permission
        if req.sort is not None and req.sort != "":
            filters[FilterOperators.EQ]["sort"] = req.sort
        if req.path is not None and req.path != "":
            filters[FilterOperators.EQ]["path"] = req.path
        if req.component is not None and req.component != "":
            filters[FilterOperators.EQ]["component"] = req.component
        if req.type is not None and req.type != "":
            filters[FilterOperators.EQ]["type"] = req.type
        if req.cacheable is not None and req.cacheable != "":
            filters[FilterOperators.EQ]["cacheable"] = req.cacheable
        if req.visible is not None and req.visible != "":
            filters[FilterOperators.EQ]["visible"] = req.visible
        if req.status is not None and req.status != "":
            filters[FilterOperators.EQ]["status"] = req.status
        if req.create_time is not None and req.create_time != "":
            filters[FilterOperators.EQ]["create_time"] = req.create_time
        sort_list = None
        sort_str = req.sort_str
        if sort_str is not None:
            sort_list = json.loads(sort_str)
        return await self.mapper.select_by_ordered_page(
            current=req.current,
            page_size=req.page_size,
            count=req.count,
            **filters,
            sort_list=sort_list,
        )

    async def get_children_recursively(
        self, *, parent_data: list[MenuModel], schema_class: Type[Menu]
    ) -> list[Menu]:
        if not parent_data:
            return []
        menu_list = [Menu(**record.model_dump()) for record in parent_data]
        return await self.mapper.get_children_recursively(
            parent_data=menu_list, schema_class=schema_class
        )

    async def create_menu(self, req: CreateMenuRequest) -> MenuModel:
        menu_record: MenuModel = await self.mapper.select_by_name(
            name=req.menu.name
        )
        if menu_record is not None:
            raise BusinessException(BusinessErrorCode.MENU_NAME_EXISTS)
        menu: MenuModel = MenuModel(**req.menu.model_dump())
        return await self.save(data=menu)

    async def update_menu(self, req: UpdateMenuRequest) -> MenuModel:
        menu_record: MenuModel = await self.retrieve_by_id(id=req.menu.id)
        if menu_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        menu_model = MenuModel(**req.menu.model_dump(exclude_unset=True))
        await self.modify_by_id(data=menu_model)
        merged_data = {**menu_record.model_dump(), **menu_model.model_dump()}
        return MenuModel(**merged_data)

    async def delete_menu(self, id: int) -> None:
        menu_record: MenuModel = await self.retrieve_by_id(id=id)
        if menu_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.delete_by_id(id=id)

    async def batch_get_menus(self, ids: list[int]) -> list[MenuModel]:
        menu_records = list[MenuModel] = await self.retrieve_by_ids(ids=ids)
        if menu_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(menu_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in menu_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(menu_records)} != {str(not_exits_ids)}",
            )
        return menu_records

    async def batch_create_menus(
        self,
        *,
        req: BatchCreateMenuRequest,
    ) -> list[MenuModel]:
        menu_list: list[CreateMenu] = req.menus
        if not menu_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        menu_names = [menu.name for menu in menu_list]
        menu_records: list[MenuModel] = await self.mapper.select_by_names(
            names=menu_names
        )
        if menu_records:
            exist_menu_names = [menu.name for menu in menu_records]
            raise BusinessException(
                BusinessErrorCode.MENU_NAME_EXISTS,
                f"{BusinessErrorCode.MENU_NAME_EXISTS.message}: {str(exist_menu_names)}",
            )
        data_list = [MenuModel(**menu.model_dump()) for menu in menu_list]
        await self.batch_save(data=data_list)
        return data_list

    async def export_menu_page(
        self, *, ids: list[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        menu_list: list[MenuModel] = await self.retrieve_by_ids(ids=ids)
        if menu_list is None or len(menu_list) == 0:
            return None
        menu_page_list = [Menu(**menu.model_dump()) for menu in menu_list]
        return await excel_util.export_excel(
            schema=Menu,
            file_name="menu_data_export",
            data_list=menu_page_list,
        )

    async def batch_create_menu(
        self,
        *,
        menu_create_list: list[CreateMenuRequest],
        current_user: CurrentUser,
    ) -> list[int]:
        menu_list: list[MenuModel] = [
            MenuModel(**menu_create.model_dump())
            for menu_create in menu_create_list
        ]
        await self.batch_save(data_list=menu_list)
        return [menu.id for menu in menu_list]

    @staticmethod
    async def import_menu(
        *, file: UploadFile, current_user: CurrentUser
    ) -> Union[list[CreateMenuRequest], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        menu_records = import_df.to_dict(orient="records")
        if menu_records is None or len(menu_records) == 0:
            return None
        for record in menu_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        menu_create_list = []
        for menu_record in menu_records:
            try:
                menu_create = CreateMenuRequest(**menu_record)
                menu_create_list.append(menu_create)
            except Exception as e:
                valid_data = {
                    k: v
                    for k, v in menu_record.items()
                    if k in CreateMenuRequest.model_fields
                }
                menu_create = CreateMenuRequest.model_construct(**valid_data)
                menu_create.err_msg = ValidateService.get_validate_err_msg(e)
                menu_create_list.append(menu_create)
                return menu_create_list

        return menu_create_list

    async def batch_remove_menus(self, req: BatchDeleteMenusRequest):
        ids: list[int] = req.ids
        await self.delete_by_ids(ids=ids)

    async def import_menus(self, req: ImportMenusRequest) -> list[ImportMenu]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        menu_records = import_df.to_dict(orient="records")
        if menu_records is None or len(menu_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in menu_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        menu_import_list = []
        for menu_record in menu_records:
            try:
                menu_create = ImportMenu(**menu_record)
                menu_import_list.append(menu_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in menu_record.items()
                    if k in ImportMenu.model_fields
                }
                menu_create = ImportMenu.model_construct(**valid_data)
                menu_create.err_msg = ValidateService.get_validate_err_msg(e)
                menu_import_list.append(menu_create)
                return menu_import_list

        return menu_import_list

    async def export_menus_template(self) -> StreamingResponse:
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        file_name = f"menu_import_tpl_{timestamp}"
        return await excel_util.export_excel(
            schema=CreateMenu, file_name=file_name
        )

    async def batch_update_menus(
        self, req: BatchUpdateMenusRequest
    ) -> list[MenuModel]:
        menus: list[UpdateMenu] = req.menus
        if not menus:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            menu.model_dump(exclude_unset=True) for menu in menus
        ]
        await self.mapper.batch_update(items=update_data)
        menu_ids: list[int] = [menu.id for menu in menus]
        return await self.mapper.select_by_ids(ids=menu_ids)

    async def export_menus(self, req: ExportMenusRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        menu_list: list[MenuModel] = await self.mapper.select_by_ids(ids=ids)
        if menu_list is None or len(menu_list) == 0:
            logger.error(f"No menus found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        menu_page_list = [ExportMenu(**menu.model_dump()) for menu in menu_list]
        file_name = "menu_data_export"
        return await excel_util.export_excel(
            schema=ExportMenu, file_name=file_name, data_list=menu_page_list
        )
