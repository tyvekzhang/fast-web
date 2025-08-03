# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
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
"""domain service impl"""

from __future__ import annotations

import io
import json
from typing import Type, Any

import pandas as pd
from loguru import logger
from pydantic import ValidationError
from starlette.responses import StreamingResponse

from src.main.app.core.constant import FilterOperators
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.core.utils import excel_util
from src.main.app.core.utils.validate_util import ValidateService
from src.main.app.enums import BusinessErrorCode
from src.main.app.exception.biz_exception import BusinessException
from src.main.app.mapper.system.role_menu_mapper import RoleMenuMapper
from src.main.app.model.system.role_menu_model import RoleMenuModel
from src.main.app.schema.system.role_menu_schema import (
    ListRoleMenusRequest,
    RoleMenu,
    CreateRoleMenuRequest,
    UpdateRoleMenuRequest,
    BatchDeleteRoleMenusRequest,
    ExportRoleMenusRequest,
    BatchCreateRoleMenusRequest,
    CreateRoleMenu,
    BatchUpdateRoleMenusRequest,
    UpdateRoleMenu,
    ImportRoleMenusRequest,
    ImportRoleMenu,
    ExportRoleMenu,
    BatchPatchRoleMenusRequest,
    BatchUpdateRoleMenu,
)
from src.main.app.service.system.role_menu_service import RoleMenuService


class RoleMenuServiceImpl(BaseServiceImpl[RoleMenuMapper, RoleMenuModel], RoleMenuService):
    """
    Implementation of the RoleMenuService interface.
    """

    def __init__(self, mapper: RoleMenuMapper):
        """
        Initialize the RoleMenuServiceImpl instance.

        Args:
            mapper (RoleMenuMapper): The RoleMenuMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def get_role_menu(
        self,
        *,
        id: int,
    ) -> RoleMenuModel:
        role_menu_record: RoleMenuModel = await self.mapper.select_by_id(id=id)
        if role_menu_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return role_menu_record

    async def list_role_menus(self, req: ListRoleMenusRequest) -> tuple[list[RoleMenuModel], int]:
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
        if req.id is not None and req.id != "":
            filters[FilterOperators.EQ]["id"] = req.id
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
        self, *, parent_data: list[RoleMenuModel], schema_class: Type[RoleMenu]
    ) -> list[RoleMenu]:
        if not parent_data:
            return []
        role_menu_list = [RoleMenu(**record.model_dump()) for record in parent_data]
        return await self.mapper.get_children_recursively(
            parent_data=role_menu_list, schema_class=schema_class
        )

    async def create_role_menu(self, req: CreateRoleMenuRequest) -> RoleMenuModel:
        role_menu: RoleMenuModel = RoleMenuModel(**req.role_menu.model_dump())
        return await self.save(data=role_menu)

    async def update_role_menu(self, req: UpdateRoleMenuRequest) -> RoleMenuModel:
        role_menu_record: RoleMenuModel = await self.retrieve_by_id(id=req.role_menu.id)
        if role_menu_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        role_menu_model = RoleMenuModel(**req.role_menu.model_dump(exclude_unset=True))
        await self.modify_by_id(data=role_menu_model)
        merged_data = {**role_menu_record.model_dump(), **role_menu_model.model_dump()}
        return RoleMenuModel(**merged_data)

    async def delete_role_menu(self, id: int) -> None:
        role_menu_record: RoleMenuModel = await self.retrieve_by_id(id=id)
        if role_menu_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_role_menus(self, ids: list[int]) -> list[RoleMenuModel]:
        role_menu_records = list[RoleMenuModel] = await self.retrieve_by_ids(ids=ids)
        if role_menu_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(role_menu_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in role_menu_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(role_menu_records)} != {str(not_exits_ids)}",
            )
        return role_menu_records

    async def batch_create_role_menus(
        self,
        *,
        req: BatchCreateRoleMenusRequest,
    ) -> list[RoleMenuModel]:
        role_menu_list: list[CreateRoleMenu] = req.role_menus
        if not role_menu_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [RoleMenuModel(**role_menu.model_dump()) for role_menu in role_menu_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_role_menus(
        self, req: BatchUpdateRoleMenusRequest
    ) -> list[RoleMenuModel]:
        role_menu: BatchUpdateRoleMenu = req.role_menu
        ids: list[int] = req.ids
        if not role_menu or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(ids=ids, data=role_menu.model_dump(exclude_none=True))
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_role_menus(self, req: BatchPatchRoleMenusRequest) -> list[RoleMenuModel]:
        role_menus: list[UpdateRoleMenu] = req.role_menus
        if not role_menus:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            role_menu.model_dump(exclude_unset=True) for role_menu in role_menus
        ]
        await self.mapper.batch_update(items=update_data)
        role_menu_ids: list[int] = [role_menu.id for role_menu in role_menus]
        return await self.mapper.select_by_ids(ids=role_menu_ids)

    async def batch_delete_role_menus(self, req: BatchDeleteRoleMenusRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_role_menus_template(self) -> StreamingResponse:
        file_name = "role_menu_import_tpl"
        return await excel_util.export_excel(schema=CreateRoleMenu, file_name=file_name)

    async def export_role_menus(self, req: ExportRoleMenusRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        role_menu_list: list[RoleMenuModel] = await self.mapper.select_by_ids(ids=ids)
        if role_menu_list is None or len(role_menu_list) == 0:
            logger.error(f"No role_menus found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        role_menu_page_list = [
            ExportRoleMenu(**role_menu.model_dump()) for role_menu in role_menu_list
        ]
        file_name = "role_menu_data_export"
        return await excel_util.export_excel(
            schema=ExportRoleMenu, file_name=file_name, data_list=role_menu_page_list
        )

    async def import_role_menus(self, req: ImportRoleMenusRequest) -> list[ImportRoleMenu]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        role_menu_records = import_df.to_dict(orient="records")
        if role_menu_records is None or len(role_menu_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in role_menu_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        role_menu_import_list = []
        for role_menu_record in role_menu_records:
            try:
                role_menu_create = ImportRoleMenu(**role_menu_record)
                role_menu_import_list.append(role_menu_create)
            except ValidationError as e:
                valid_data = {
                    k: v for k, v in role_menu_record.items() if k in ImportRoleMenu.model_fields
                }
                role_menu_create = ImportRoleMenu.model_construct(**valid_data)
                role_menu_create.err_msg = ValidateService.get_validate_err_msg(e)
                role_menu_import_list.append(role_menu_create)
                return role_menu_import_list

        return role_menu_import_list
