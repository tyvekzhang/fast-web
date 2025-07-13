"""DictType domain service impl"""

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
from src.main.app.mapper.sys_dict_type_mapper import DictTypeMapper
from src.main.app.model.sys_dict_type_model import DictTypeModel
from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.schema.sys_dict_type_schema import (
    DictTypeQuery,
    DictTypePage,
    DictTypeDetail,
    DictTypeCreate,
)
from src.main.app.core.service.impl.base_service_impl import BaseServiceImpl
from src.main.app.service.sys_dict_type_service import DictTypeService


class DictTypeServiceImpl(
    BaseServiceImpl[DictTypeMapper, DictTypeModel], DictTypeService
):
    """
    Implementation of the DictTypeService interface.
    """

    def __init__(self, mapper: DictTypeMapper):
        """
        Initialize the DictTypeServiceImpl instance.

        Args:
            mapper (DictTypeMapper): The DictTypeMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def get_dict_type_by_page(
        self, dict_type_query: DictTypeQuery, current_user: CurrentUser
    ) -> PageResult:
        eq = {}
        ne = {}
        gt = {}
        ge = {}
        lt = {}
        le = {}
        between = {}
        like = {}
        if dict_type_query.id is not None and dict_type_query.id != "":
            eq["id"] = dict_type_query.id
        if dict_type_query.name is not None and dict_type_query.name != "":
            like["name"] = dict_type_query.name
        if dict_type_query.type is not None and dict_type_query.type != "":
            eq["type"] = dict_type_query.type
        if dict_type_query.status is not None and dict_type_query.status != "":
            eq["status"] = dict_type_query.status
        if (
            dict_type_query.create_time is not None
            and dict_type_query.create_time != ""
        ):
            eq["create_time"] = dict_type_query.create_time
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
            current=dict_type_query.current,
            page_size=dict_type_query.page_size,
            **filters,
        )
        if total == 0:
            return PageResult(records=[], total=total)
        if "sort" in DictTypeModel.model_fields and total > 1:
            records.sort(key=lambda x: x["sort"])
        records = [DictTypePage(**record.model_dump()) for record in records]
        return PageResult(records=records, total=total)

    async def get_dict_type_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[DictTypeDetail]:
        dict_type_do: DictTypeModel = await self.mapper.select_by_id(id=id)
        if dict_type_do is None:
            return None
        return DictTypeDetail(**dict_type_do.model_dump())

    async def export_dict_type_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]:
        if ids is None or len(ids) == 0:
            return None
        dict_type_list: List[DictTypeModel] = await self.retrieve_by_ids(
            ids=ids
        )
        if dict_type_list is None or len(dict_type_list) == 0:
            return None
        dict_type_page_list = [
            DictTypePage(**dict_type.model_dump())
            for dict_type in dict_type_list
        ]
        return await excel_util.export_excel(
            schema=DictTypePage,
            file_name="dict_type_data_export",
            data_list=dict_type_page_list,
        )

    async def create_dict_type(
        self, dict_type_create: DictTypeCreate, current_user: CurrentUser
    ) -> DictTypeModel:
        dict_type: DictTypeModel = DictTypeModel(
            **dict_type_create.model_dump()
        )
        # dict_type.user_id = request.state.user_id
        return await self.save(data=dict_type)

    async def batch_create_dict_type(
        self,
        *,
        dict_type_create_list: List[DictTypeCreate],
        current_user: CurrentUser,
    ) -> List[int]:
        dict_type_list: List[DictTypeModel] = [
            DictTypeModel(**dict_type_create.model_dump())
            for dict_type_create in dict_type_create_list
        ]
        await self.batch_save(data_list=dict_type_list)
        return [dict_type.id for dict_type in dict_type_list]

    @staticmethod
    async def import_dict_type(
        *, file: UploadFile, current_user: CurrentUser
    ) -> Union[List[DictTypeCreate], None]:
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        dict_type_records = import_df.to_dict(orient="records")
        if dict_type_records is None or len(dict_type_records) == 0:
            return None
        for record in dict_type_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        dict_type_create_list = []
        for dict_type_record in dict_type_records:
            try:
                dict_type_create = DictTypeCreate(**dict_type_record)
                dict_type_create_list.append(dict_type_create)
            except Exception as e:
                valid_data = {
                    k: v
                    for k, v in dict_type_record.items()
                    if k in DictTypeCreate.model_fields
                }
                dict_type_create = DictTypeCreate.model_construct(**valid_data)
                dict_type_create.err_msg = ValidateService.get_validate_err_msg(
                    e
                )
                dict_type_create_list.append(dict_type_create)
                return dict_type_create_list

        return dict_type_create_list
