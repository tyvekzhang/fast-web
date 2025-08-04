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
from src.main.app.mapper.dict_datum_mapper import DictDatumMapper
from src.main.app.model.dict_datum_model import DictDatumModel
from src.main.app.schema.dict_datum_schema import (
    ListDictDataRequest,
    DictDatum,
    CreateDictDatumRequest,
    UpdateDictDatumRequest,
    BatchDeleteDictDataRequest,
    ExportDictDataRequest,
    BatchCreateDictDataRequest,
    CreateDictDatum,
    BatchUpdateDictDataRequest,
    UpdateDictDatum,
    ImportDictDataRequest,
    ImportDictDatum,
    ExportDictDatum,
    BatchPatchDictDataRequest,
    BatchUpdateDictDatum,
)
from src.main.app.service.dict_datum_service import DictDatumService


class DictDatumServiceImpl(BaseServiceImpl[DictDatumMapper, DictDatumModel], DictDatumService):
    """
    Implementation of the DictDatumService interface.
    """

    def __init__(self, mapper: DictDatumMapper):
        """
        Initialize the DictDatumServiceImpl instance.

        Args:
            mapper (DictDatumMapper): The DictDatumMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def get_dict_datum(
        self,
        *,
        id: int,
    ) -> DictDatumModel:
        dict_datum_record: DictDatumModel = await self.mapper.select_by_id(id=id)
        if dict_datum_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return dict_datum_record

    async def list_dict_data(self, req: ListDictDataRequest) -> tuple[list[DictDatumModel], int]:
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
        if req.label is not None and req.label != "":
            filters[FilterOperators.EQ]["label"] = req.label
        if req.value is not None and req.value != "":
            filters[FilterOperators.EQ]["value"] = req.value
        if req.type is not None and req.type != "":
            filters[FilterOperators.EQ]["type"] = req.type
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

    async def get_all_dict_data(self) -> list[DictDatumModel]:
        result = []
        current = 1
        page_size = 1000

        while True:
            items, total = await self.mapper.select_by_ordered_page(
                current=current,
                page_size=page_size,
            )
            result.extend(items)
            if len(items) == total:
                break
            current += 1

        return result

    async def get_dict_options(self, req: list[str]) -> list[DictDatumModel]:
        return await self.mapper.select_by_types(data=req)

    async def create_dict_datum(self, req: CreateDictDatumRequest) -> DictDatumModel:
        dict_datum: DictDatumModel = DictDatumModel(**req.dict_datum.model_dump())
        return await self.save(data=dict_datum)

    async def update_dict_datum(self, req: UpdateDictDatumRequest) -> DictDatumModel:
        dict_datum_record: DictDatumModel = await self.retrieve_by_id(id=req.dict_datum.id)
        if dict_datum_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        dict_datum_model = DictDatumModel(**req.dict_datum.model_dump(exclude_unset=True))
        await self.modify_by_id(data=dict_datum_model)
        merged_data = {**dict_datum_record.model_dump(), **dict_datum_model.model_dump()}
        return DictDatumModel(**merged_data)

    async def delete_dict_datum(self, id: int) -> None:
        dict_datum_record: DictDatumModel = await self.retrieve_by_id(id=id)
        if dict_datum_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_dict_data(self, ids: list[int]) -> list[DictDatumModel]:
        dict_datum_records = list[DictDatumModel] = await self.retrieve_by_ids(ids=ids)
        if dict_datum_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(dict_datum_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in dict_datum_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(dict_datum_records)} != {str(not_exits_ids)}",
            )
        return dict_datum_records

    async def batch_create_dict_data(
        self,
        *,
        req: BatchCreateDictDataRequest,
    ) -> list[DictDatumModel]:
        dict_datum_list: list[CreateDictDatum] = req.dict_data
        if not dict_datum_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [DictDatumModel(**dict_datum.model_dump()) for dict_datum in dict_datum_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_dict_data(self, req: BatchUpdateDictDataRequest) -> list[DictDatumModel]:
        dict_datum: BatchUpdateDictDatum = req.dict_datum
        ids: list[int] = req.ids
        if not dict_datum or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=dict_datum.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_dict_data(self, req: BatchPatchDictDataRequest) -> list[DictDatumModel]:
        dict_data: list[UpdateDictDatum] = req.dict_data
        if not dict_data:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            dict_datum.model_dump(exclude_unset=True) for dict_datum in dict_data
        ]
        await self.mapper.batch_update(items=update_data)
        dict_datum_ids: list[int] = [dict_datum.id for dict_datum in dict_data]
        return await self.mapper.select_by_ids(ids=dict_datum_ids)

    async def batch_delete_dict_data(self, req: BatchDeleteDictDataRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_dict_data_template(self) -> StreamingResponse:
        file_name = "dict_datum_import_tpl"
        return await excel_util.export_excel(schema=CreateDictDatum, file_name=file_name)

    async def export_dict_data(self, req: ExportDictDataRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        dict_datum_list: list[DictDatumModel] = await self.mapper.select_by_ids(ids=ids)
        if dict_datum_list is None or len(dict_datum_list) == 0:
            logger.error(f"No dict_data found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        dict_datum_page_list = [
            ExportDictDatum(**dict_datum.model_dump()) for dict_datum in dict_datum_list
        ]
        file_name = "dict_datum_data_export"
        return await excel_util.export_excel(
            schema=ExportDictDatum, file_name=file_name, data_list=dict_datum_page_list
        )

    async def import_dict_data(self, req: ImportDictDataRequest) -> list[ImportDictDatum]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        dict_datum_records = import_df.to_dict(orient="records")
        if dict_datum_records is None or len(dict_datum_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in dict_datum_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        dict_datum_import_list = []
        for dict_datum_record in dict_datum_records:
            try:
                dict_datum_create = ImportDictDatum(**dict_datum_record)
                dict_datum_import_list.append(dict_datum_create)
            except ValidationError as e:
                valid_data = {
                    k: v for k, v in dict_datum_record.items() if k in ImportDictDatum.model_fields
                }
                dict_datum_create = ImportDictDatum.model_construct(**valid_data)
                dict_datum_create.err_msg = ValidateService.get_validate_err_msg(e)
                dict_datum_import_list.append(dict_datum_create)
                return dict_datum_import_list

        return dict_datum_import_list
