"""Role domain service impl"""

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
from src.main.app.mapper.sys_role_mapper import RoleMapper
from src.main.app.model.sys_role_model import RoleModel
from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.schema.sys_role_schema import (
    RoleQuery,
    RolePage,
    RoleDetail,
    RoleCreate,
)
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.service.sys_role_service import RoleService


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

    async def get_role_by_page(
        self, role_query: RoleQuery, current_user: CurrentUser
    ) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if role_query.id is not None and role_query.id != "":
            eq["id"] = role_query.id
        if role_query.name is not None and role_query.name != "":
            like["name"] = role_query.name
        if role_query.code is not None and role_query.code != "":
            eq["code"] = role_query.code
        if role_query.sort is not None and role_query.sort != "":
            eq["sort"] = role_query.sort
        if role_query.data_scope is not None and role_query.data_scope != "":
            eq["data_scope"] = role_query.data_scope
        if role_query.status is not None and role_query.status != "":
            eq["status"] = role_query.status
        if role_query.create_time is not None and role_query.create_time != "":
            eq["create_time"] = role_query.create_time
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
            current=role_query.current, page_size=role_query.page_size, **filters
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in RoleModel.model_fields and total > 1:
            records.sort(key=lambda x: x["sort"])
        records = [RolePage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def get_role_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[RoleDetail]:
        role_do: RoleModel = await self.mapper.select_by_id(id=id)
        if role_do is None:
            return None
        return RoleDetail(**role_do.model_dump())

    async def export_role_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        role_list: List[RoleModel] = await self.retrieve_by_ids(ids=ids)
        if role_list is None or len(role_list) == 0:
            return None
        role_page_list = [RolePage(**role.model_dump()) for role in role_list]
        return await excel_util.export_excel(
            schema=RolePage,
            file_name="role_data_export",
            data_list=role_page_list,
        )

    async def create_role(
        self, role_create: RoleCreate, current_user: CurrentUser
    ) -> RoleModel:
        role: RoleModel = RoleModel(**role_create.model_dump())
        # role.user_id = request.state.user_id
        return await self.save(data=role)

    async def batch_create_role(
        self, *, role_create_list: List[RoleCreate], current_user: CurrentUser
    ) -> List[int]:
        role_list: List[RoleModel] = [
            RoleModel(**role_create.model_dump())
            for role_create in role_create_list
        ]
        await self.batch_save(data_list=role_list)
        return [role.id for role in role_list]

    @staticmethod
    async def import_role(
        *, file: UploadFile, current_user: CurrentUser
    ) -> Union[List[RoleCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        role_records = import_df.to_dict(orient="records")
        if role_records is None or len(role_records) == 0:
            return None
        for record in role_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        role_create_list = []
        for role_record in role_records:
            try:
                role_create = RoleCreate(**role_record)
                role_create_list.append(role_create)
            except Exception as e:
                valid_data = {
                    k: v
                    for k, v in role_record.items()
                    if k in RoleCreate.model_fields
                }
                role_create = RoleCreate.model_construct(**valid_data)
                role_create.err_msg = ValidateService.get_validate_err_msg(e)
                role_create_list.append(role_create)
                return role_create_list

        return role_create_list
