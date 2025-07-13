"""Menu domain service impl"""

from __future__ import annotations
import io
from typing import Optional, List
from typing import Union
import pandas as pd
from fastapi import UploadFile
from starlette.responses import StreamingResponse
from src.main.app.core.constant import FilterOperators
from src.main.app.core.utils import excel_util
from src.main.app.core.utils.validate_util import ValidateService
from src.main.app.mapper.sys_menu_mapper import MenuMapper
from src.main.app.model.sys_menu_model import MenuModel
from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.schema.sys_menu_schema import (
    ListMenuRequest,
    Menu,
    MenuDetail,
    MenuCreate,
)
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.service.sys_menu_service import MenuService


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

    async def list_menus(
        self, req: ListMenuRequest
    ) -> PageResult[Menu]:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if req.parent_id is not None and req.parent_id != "":
            eq["parent_id"] = req.parent_id
        if req.id is not None and req.id != "":
            eq["id"] = req.id
        if req.name is not None and req.name != "":
            like["name"] = req.name
        if req.icon is not None and req.icon != "":
            eq["icon"] = req.icon
        if req.permission is not None and req.permission != "":
            eq["permission"] = req.permission
        if req.sort is not None and req.sort != "":
            eq["sort"] = req.sort
        if req.path is not None and req.path != "":
            eq["path"] = req.path
        if req.component is not None and req.component != "":
            eq["component"] = req.component
        if req.type is not None and req.type != "":
            eq["type"] = req.type
        if req.cacheable is not None and req.cacheable != "":
            eq["cacheable"] = req.cacheable
        if req.visible is not None and req.visible != "":
            eq["visible"] = req.visible
        if req.status is not None and req.status != "":
            eq["status"] = req.status
        if req.create_time is not None and req.create_time != "":
            eq["create_time"] = req.create_time
        filters = {
            FilterOperators.EQ: eq,
            FilterOperators.NE: ne,
            FilterOperators.GT: gt,
            FilterOperators.GE: ge,
            FilterOperators.LT: lt,
            FilterOperators.LE: le,
            FilterOperators.BETWEEN: between,
            FilterOperators.LIKE: like,
        }
        records, total = await self.mapper.select_by_ordered_page(
            current=req.current, page_size=req.page_size, **filters
        )
        if records is None or len(records) == 0:
            return PageResult(records=[], total=total)
        records = [Menu(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def get_menu_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[MenuDetail]:
        menu_do: MenuModel = await self.mapper.select_by_id(id=id)
        if menu_do is None:
            return None
        return MenuDetail(**menu_do.model_dump())

    async def export_menu_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        menu_list: List[MenuModel] = await self.retrieve_by_ids(ids=ids)
        if menu_list is None or len(menu_list) == 0:
            return None
        menu_page_list = [Menu(**menu.model_dump()) for menu in menu_list]
        return await excel_util.export_excel(
            schema=Menu,
            file_name="menu_data_export",
            data_list=menu_page_list,
        )

    async def create_menu(
        self, menu_create: MenuCreate, current_user: CurrentUser
    ) -> MenuModel:
        menu: MenuModel = MenuModel(**menu_create.model_dump())
        # menu.user_id = request.state.user_id
        return await self.save(data=menu)

    async def batch_create_menu(
        self, *, menu_create_list: List[MenuCreate], current_user: CurrentUser
    ) -> List[int]:
        menu_list: List[MenuModel] = [
            MenuModel(**menu_create.model_dump())
            for menu_create in menu_create_list
        ]
        await self.batch_save(data_list=menu_list)
        return [menu.id for menu in menu_list]

    @staticmethod
    async def import_menu(
        *, file: UploadFile, current_user: CurrentUser
    ) -> Union[List[MenuCreate], None]:
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
                menu_create = MenuCreate(**menu_record)
                menu_create_list.append(menu_create)
            except Exception as e:
                valid_data = {
                    k: v
                    for k, v in menu_record.items()
                    if k in MenuCreate.model_fields
                }
                menu_create = MenuCreate.model_construct(**valid_data)
                menu_create.err_msg = ValidateService.get_validate_err_msg(e)
                menu_create_list.append(menu_create)
                return menu_create_list

        return menu_create_list
