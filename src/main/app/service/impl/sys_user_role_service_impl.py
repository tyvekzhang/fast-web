"""UserRole domain service impl"""

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
from src.main.app.mapper.sys_user_role_mapper import UserRoleMapper
from src.main.app.model.sys_user_role_model import UserRoleModel
from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.schema.sys_user_role_schema import (
    UserRoleQuery,
    UserRolePage,
    UserRoleDetail,
    UserRoleCreate,
)
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.service.sys_user_role_service import UserRoleService


class UserRoleServiceImpl(
    BaseServiceImpl[UserRoleMapper, UserRoleModel], UserRoleService
):
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

    async def get_user_role_by_page(
        self, user_role_query: UserRoleQuery, current_user: CurrentUser
    ) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if user_role_query.id is not None and user_role_query.id != "":
            eq["id"] = user_role_query.id
        if (
            user_role_query.create_time is not None
            and user_role_query.create_time != ""
        ):
            eq["create_time"] = user_role_query.create_time
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
            current=user_role_query.current,
            page_size=user_role_query.page_size,
            **filters,
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in UserRoleModel.model_fields and total > 1:
            records.sort(key=lambda x: x["sort"])
        records = [UserRolePage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def get_user_role_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[UserRoleDetail]:
        user_role_do: UserRoleModel = await self.mapper.select_by_id(id=id)
        if user_role_do is None:
            return None
        return UserRoleDetail(**user_role_do.model_dump())

    async def export_user_role_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        user_role_list: List[UserRoleModel] = await self.retrieve_by_ids(
            ids=ids
        )
        if user_role_list is None or len(user_role_list) == 0:
            return None
        user_role_page_list = [
            UserRolePage(**user_role.model_dump())
            for user_role in user_role_list
        ]
        return await excel_util.export_excel(
            schema=UserRolePage,
            file_name="user_role_data_export",
            data_list=user_role_page_list,
        )

    async def create_user_role(
        self, user_role_create: UserRoleCreate, current_user: CurrentUser
    ) -> UserRoleModel:
        user_role: UserRoleModel = UserRoleModel(
            **user_role_create.model_dump()
        )
        # user_role.user_id = request.state.user_id
        return await self.save(data=user_role)

    async def batch_create_user_role(
        self,
        *,
        user_role_create_list: List[UserRoleCreate],
        current_user: CurrentUser,
    ) -> List[int]:
        user_role_list: List[UserRoleModel] = [
            UserRoleModel(**user_role_create.model_dump())
            for user_role_create in user_role_create_list
        ]
        await self.batch_save(data_list=user_role_list)
        return [user_role.id for user_role in user_role_list]

    @staticmethod
    async def import_user_role(
        *, file: UploadFile, current_user: CurrentUser
    ) -> Union[List[UserRoleCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        user_role_records = import_df.to_dict(orient="records")
        if user_role_records is None or len(user_role_records) == 0:
            return None
        for record in user_role_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        user_role_create_list = []
        for user_role_record in user_role_records:
            try:
                user_role_create = UserRoleCreate(**user_role_record)
                user_role_create_list.append(user_role_create)
            except Exception as e:
                valid_data = {
                    k: v
                    for k, v in user_role_record.items()
                    if k in UserRoleCreate.model_fields
                }
                user_role_create = UserRoleCreate.model_construct(**valid_data)
                user_role_create.err_msg = ValidateService.get_validate_err_msg(
                    e
                )
                user_role_create_list.append(user_role_create)
                return user_role_create_list

        return user_role_create_list
