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
from src.main.app.mapper.role_mapper import RoleMapper
from src.main.app.model.role_model import RoleModel
from src.main.app.schema.role_schema import (
    ListRolesRequest,
    Role,
    CreateRoleRequest,
    UpdateRoleRequest,
    BatchDeleteRolesRequest,
    ExportRolesRequest,
    BatchCreateRolesRequest,
    CreateRole,
    BatchUpdateRolesRequest,
    UpdateRole,
    ImportRolesRequest,
    ImportRole,
    ExportRole,
    BatchPatchRolesRequest,
    BatchUpdateRole,
)
from src.main.app.service.role_service import RoleService


class RoleServiceImpl(BaseServiceImpl[RoleMapper, RoleModel], RoleService):
    """
    Implementation of the RoleService interface.
    """

    def __init__(self, mapper: RoleMapper):
        """
        Initialize the RoleServiceImpl instance.

        Args:
            mapper (RoleMapper): The RoleMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def get_role(
        self,
        *,
        id: int,
    ) -> RoleModel:
        role_record: RoleModel = await self.mapper.select_by_id(id=id)
        if role_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return role_record

    async def list_roles(self, req: ListRolesRequest) -> tuple[list[RoleModel], int]:
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
        if req.name is not None and req.name != "":
            filters[FilterOperators.LIKE]["name"] = req.name
        if req.code is not None and req.code != "":
            filters[FilterOperators.EQ]["code"] = req.code
        if req.sort is not None and req.sort != "":
            filters[FilterOperators.EQ]["sort"] = req.sort
        if req.data_scope is not None and req.data_scope != "":
            filters[FilterOperators.EQ]["data_scope"] = req.data_scope
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
        self, *, parent_data: list[RoleModel], schema_class: Type[Role]
    ) -> list[Role]:
        if not parent_data:
            return []
        role_list = [Role(**record.model_dump()) for record in parent_data]
        return await self.mapper.get_children_recursively(
            parent_data=role_list, schema_class=schema_class
        )

    async def create_role(self, req: CreateRoleRequest) -> RoleModel:
        role: RoleModel = RoleModel(**req.role.model_dump())
        return await self.save(data=role)

    async def update_role(self, req: UpdateRoleRequest) -> RoleModel:
        role_record: RoleModel = await self.retrieve_by_id(id=req.role.id)
        if role_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        role_model = RoleModel(**req.role.model_dump(exclude_unset=True))
        await self.modify_by_id(data=role_model)
        merged_data = {**role_record.model_dump(), **role_model.model_dump()}
        return RoleModel(**merged_data)

    async def delete_role(self, id: int) -> None:
        role_record: RoleModel = await self.retrieve_by_id(id=id)
        if role_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_roles(self, ids: list[int]) -> list[RoleModel]:
        role_records = list[RoleModel] = await self.retrieve_by_ids(ids=ids)
        if role_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(role_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in role_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(role_records)} != {str(not_exits_ids)}",
            )
        return role_records

    async def batch_create_roles(
        self,
        *,
        req: BatchCreateRolesRequest,
    ) -> list[RoleModel]:
        role_list: list[CreateRole] = req.roles
        if not role_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [RoleModel(**role.model_dump()) for role in role_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_roles(self, req: BatchUpdateRolesRequest) -> list[RoleModel]:
        role: BatchUpdateRole = req.role
        ids: list[int] = req.ids
        if not role or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(ids=ids, data=role.model_dump(exclude_none=True))
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_roles(self, req: BatchPatchRolesRequest) -> list[RoleModel]:
        roles: list[UpdateRole] = req.roles
        if not roles:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [role.model_dump(exclude_unset=True) for role in roles]
        await self.mapper.batch_update(items=update_data)
        role_ids: list[int] = [role.id for role in roles]
        return await self.mapper.select_by_ids(ids=role_ids)

    async def batch_delete_roles(self, req: BatchDeleteRolesRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_roles_template(self) -> StreamingResponse:
        file_name = "role_import_tpl"
        return await excel_util.export_excel(schema=CreateRole, file_name=file_name)

    async def export_roles(self, req: ExportRolesRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        role_list: list[RoleModel] = await self.mapper.select_by_ids(ids=ids)
        if role_list is None or len(role_list) == 0:
            logger.error(f"No roles found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        role_page_list = [ExportRole(**role.model_dump()) for role in role_list]
        file_name = "role_data_export"
        return await excel_util.export_excel(
            schema=ExportRole, file_name=file_name, data_list=role_page_list
        )

    async def import_roles(self, req: ImportRolesRequest) -> list[ImportRole]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        role_records = import_df.to_dict(orient="records")
        if role_records is None or len(role_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in role_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        role_import_list = []
        for role_record in role_records:
            try:
                role_create = ImportRole(**role_record)
                role_import_list.append(role_create)
            except ValidationError as e:
                valid_data = {k: v for k, v in role_record.items() if k in ImportRole.model_fields}
                role_create = ImportRole.model_construct(**valid_data)
                role_create.err_msg = ValidateService.get_validate_err_msg(e)
                role_import_list.append(role_create)
                return role_import_list

        return role_import_list
