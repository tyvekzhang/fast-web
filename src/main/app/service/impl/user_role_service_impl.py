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
from src.main.app.mapper.user_role_mapper import UserRoleMapper
from src.main.app.model.user_role_model import UserRoleModel
from src.main.app.schema.user_role_schema import (
    ListUserRolesRequest,
    UserRole,
    CreateUserRoleRequest,
    UpdateUserRoleRequest,
    BatchDeleteUserRolesRequest,
    ExportUserRolesRequest,
    BatchCreateUserRolesRequest,
    CreateUserRole,
    BatchUpdateUserRolesRequest,
    UpdateUserRole,
    ImportUserRolesRequest,
    ImportUserRole,
    ExportUserRole,
    BatchPatchUserRolesRequest,
    BatchUpdateUserRole,
)
from src.main.app.service.user_role_service import UserRoleService


class UserRoleServiceImpl(BaseServiceImpl[UserRoleMapper, UserRoleModel], UserRoleService):
    """
    Implementation of the UserRoleService interface.
    """

    def __init__(self, mapper: UserRoleMapper):
        """
        Initialize the UserRoleServiceImpl instance.

        Args:
            mapper (UserRoleMapper): The UserRoleMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def get_user_role(
        self,
        *,
        id: int,
    ) -> UserRoleModel:
        user_role_record: UserRoleModel = await self.mapper.select_by_id(id=id)
        if user_role_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return user_role_record

    async def list_user_roles(self, req: ListUserRolesRequest) -> tuple[list[UserRoleModel], int]:
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
        self, *, parent_data: list[UserRoleModel], schema_class: Type[UserRole]
    ) -> list[UserRole]:
        if not parent_data:
            return []
        user_role_list = [UserRole(**record.model_dump()) for record in parent_data]
        return await self.mapper.get_children_recursively(
            parent_data=user_role_list, schema_class=schema_class
        )

    async def create_user_role(self, req: CreateUserRoleRequest) -> UserRoleModel:
        user_role: UserRoleModel = UserRoleModel(**req.user_role.model_dump())
        return await self.save(data=user_role)

    async def update_user_role(self, req: UpdateUserRoleRequest) -> UserRoleModel:
        user_role_record: UserRoleModel = await self.retrieve_by_id(id=req.user_role.id)
        if user_role_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        user_role_model = UserRoleModel(**req.user_role.model_dump(exclude_unset=True))
        await self.modify_by_id(data=user_role_model)
        merged_data = {**user_role_record.model_dump(), **user_role_model.model_dump()}
        return UserRoleModel(**merged_data)

    async def delete_user_role(self, id: int) -> None:
        user_role_record: UserRoleModel = await self.retrieve_by_id(id=id)
        if user_role_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_user_roles(self, ids: list[int]) -> list[UserRoleModel]:
        user_role_records = list[UserRoleModel] = await self.retrieve_by_ids(ids=ids)
        if user_role_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(user_role_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in user_role_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(user_role_records)} != {str(not_exits_ids)}",
            )
        return user_role_records

    async def batch_create_user_roles(
        self,
        *,
        req: BatchCreateUserRolesRequest,
    ) -> list[UserRoleModel]:
        user_role_list: list[CreateUserRole] = req.user_roles
        if not user_role_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [UserRoleModel(**user_role.model_dump()) for user_role in user_role_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_user_roles(
        self, req: BatchUpdateUserRolesRequest
    ) -> list[UserRoleModel]:
        user_role: BatchUpdateUserRole = req.user_role
        ids: list[int] = req.ids
        if not user_role or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(ids=ids, data=user_role.model_dump(exclude_none=True))
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_user_roles(self, req: BatchPatchUserRolesRequest) -> list[UserRoleModel]:
        user_roles: list[UpdateUserRole] = req.user_roles
        if not user_roles:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            user_role.model_dump(exclude_unset=True) for user_role in user_roles
        ]
        await self.mapper.batch_update(items=update_data)
        user_role_ids: list[int] = [user_role.id for user_role in user_roles]
        return await self.mapper.select_by_ids(ids=user_role_ids)

    async def batch_delete_user_roles(self, req: BatchDeleteUserRolesRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_user_roles_template(self) -> StreamingResponse:
        file_name = "user_role_import_tpl"
        return await excel_util.export_excel(schema=CreateUserRole, file_name=file_name)

    async def export_user_roles(self, req: ExportUserRolesRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        user_role_list: list[UserRoleModel] = await self.mapper.select_by_ids(ids=ids)
        if user_role_list is None or len(user_role_list) == 0:
            logger.error(f"No user_roles found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        user_role_page_list = [
            ExportUserRole(**user_role.model_dump()) for user_role in user_role_list
        ]
        file_name = "user_role_data_export"
        return await excel_util.export_excel(
            schema=ExportUserRole, file_name=file_name, data_list=user_role_page_list
        )

    async def import_user_roles(self, req: ImportUserRolesRequest) -> list[ImportUserRole]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        user_role_records = import_df.to_dict(orient="records")
        if user_role_records is None or len(user_role_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in user_role_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        user_role_import_list = []
        for user_role_record in user_role_records:
            try:
                user_role_create = ImportUserRole(**user_role_record)
                user_role_import_list.append(user_role_create)
            except ValidationError as e:
                valid_data = {
                    k: v for k, v in user_role_record.items() if k in ImportUserRole.model_fields
                }
                user_role_create = ImportUserRole.model_construct(**valid_data)
                user_role_create.err_msg = ValidateService.get_validate_err_msg(e)
                user_role_import_list.append(user_role_create)
                return user_role_import_list

        return user_role_import_list
