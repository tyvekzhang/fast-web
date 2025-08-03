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
from src.main.app.mapper.codegen.dict_type_mapper import DictTypeMapper
from src.main.app.model.codegen.dict_type_model import DictTypeModel
from src.main.app.schema.codegen.dict_type_schema import (
    ListDictTypesRequest,
    DictType,
    CreateDictTypeRequest,
    UpdateDictTypeRequest,
    BatchDeleteDictTypesRequest,
    ExportDictTypesRequest,
    BatchCreateDictTypesRequest,
    CreateDictType,
    BatchUpdateDictTypesRequest,
    UpdateDictType,
    ImportDictTypesRequest,
    ImportDictType,
    ExportDictType,
    BatchPatchDictTypesRequest,
    BatchUpdateDictType,
)
from src.main.app.service.codegen.dict_type_service import DictTypeService


class DictTypeServiceImpl(BaseServiceImpl[DictTypeMapper, DictTypeModel], DictTypeService):
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

    async def get_dict_type(
        self,
        *,
        id: int,
    ) -> DictTypeModel:
        dict_type_record: DictTypeModel = await self.mapper.select_by_id(id=id)
        if dict_type_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return dict_type_record

    async def list_dict_types(self, req: ListDictTypesRequest) -> tuple[list[DictTypeModel], int]:
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
        if req.type is not None and req.type != "":
            filters[FilterOperators.EQ]["type"] = req.type
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
        self, *, parent_data: list[DictTypeModel], schema_class: Type[DictType]
    ) -> list[DictType]:
        if not parent_data:
            return []
        dict_type_list = [DictType(**record.model_dump()) for record in parent_data]
        return await self.mapper.get_children_recursively(
            parent_data=dict_type_list, schema_class=schema_class
        )

    async def create_dict_type(self, req: CreateDictTypeRequest) -> DictTypeModel:
        dict_type: DictTypeModel = DictTypeModel(**req.dict_type.model_dump())
        return await self.save(data=dict_type)

    async def update_dict_type(self, req: UpdateDictTypeRequest) -> DictTypeModel:
        dict_type_record: DictTypeModel = await self.retrieve_by_id(id=req.dict_type.id)
        if dict_type_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        dict_type_model = DictTypeModel(**req.dict_type.model_dump(exclude_unset=True))
        await self.modify_by_id(data=dict_type_model)
        merged_data = {**dict_type_record.model_dump(), **dict_type_model.model_dump()}
        return DictTypeModel(**merged_data)

    async def delete_dict_type(self, id: int) -> None:
        dict_type_record: DictTypeModel = await self.retrieve_by_id(id=id)
        if dict_type_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_dict_types(self, ids: list[int]) -> list[DictTypeModel]:
        dict_type_records = list[DictTypeModel] = await self.retrieve_by_ids(ids=ids)
        if dict_type_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(dict_type_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in dict_type_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(dict_type_records)} != {str(not_exits_ids)}",
            )
        return dict_type_records

    async def batch_create_dict_types(
        self,
        *,
        req: BatchCreateDictTypesRequest,
    ) -> list[DictTypeModel]:
        dict_type_list: list[CreateDictType] = req.dict_types
        if not dict_type_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [DictTypeModel(**dict_type.model_dump()) for dict_type in dict_type_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_dict_types(
        self, req: BatchUpdateDictTypesRequest
    ) -> list[DictTypeModel]:
        dict_type: BatchUpdateDictType = req.dict_type
        ids: list[int] = req.ids
        if not dict_type or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(ids=ids, data=dict_type.model_dump(exclude_none=True))
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_dict_types(self, req: BatchPatchDictTypesRequest) -> list[DictTypeModel]:
        dict_types: list[UpdateDictType] = req.dict_types
        if not dict_types:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            dict_type.model_dump(exclude_unset=True) for dict_type in dict_types
        ]
        await self.mapper.batch_update(items=update_data)
        dict_type_ids: list[int] = [dict_type.id for dict_type in dict_types]
        return await self.mapper.select_by_ids(ids=dict_type_ids)

    async def batch_delete_dict_types(self, req: BatchDeleteDictTypesRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_dict_types_template(self) -> StreamingResponse:
        file_name = "dict_type_import_tpl"
        return await excel_util.export_excel(schema=CreateDictType, file_name=file_name)

    async def export_dict_types(self, req: ExportDictTypesRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        dict_type_list: list[DictTypeModel] = await self.mapper.select_by_ids(ids=ids)
        if dict_type_list is None or len(dict_type_list) == 0:
            logger.error(f"No dict_types found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        dict_type_page_list = [
            ExportDictType(**dict_type.model_dump()) for dict_type in dict_type_list
        ]
        file_name = "dict_type_data_export"
        return await excel_util.export_excel(
            schema=ExportDictType, file_name=file_name, data_list=dict_type_page_list
        )

    async def import_dict_types(self, req: ImportDictTypesRequest) -> list[ImportDictType]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        dict_type_records = import_df.to_dict(orient="records")
        if dict_type_records is None or len(dict_type_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in dict_type_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        dict_type_import_list = []
        for dict_type_record in dict_type_records:
            try:
                dict_type_create = ImportDictType(**dict_type_record)
                dict_type_import_list.append(dict_type_create)
            except ValidationError as e:
                valid_data = {
                    k: v for k, v in dict_type_record.items() if k in ImportDictType.model_fields
                }
                dict_type_create = ImportDictType.model_construct(**valid_data)
                dict_type_create.err_msg = ValidateService.get_validate_err_msg(e)
                dict_type_import_list.append(dict_type_create)
                return dict_type_import_list

        return dict_type_import_list
