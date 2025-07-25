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
from src.main.app.mapper.new_word_mapper import NewWordMapper
from src.main.app.model.new_word_model import NewWordModel
from src.main.app.schema.new_word_schema import (
    ListNewWordsRequest,
    NewWord,
    CreateNewWordRequest,
    UpdateNewWordRequest,
    BatchDeleteNewWordsRequest,
    ExportNewWordsRequest,
    BatchCreateNewWordsRequest,
    CreateNewWord,
    BatchUpdateNewWordsRequest,
    UpdateNewWord,
    ImportNewWordsRequest,
    ImportNewWord,
    ExportNewWord,
    BatchPatchNewWordsRequest,
    BatchUpdateNewWord,
)
from src.main.app.service.new_word_service import NewWordService


class NewWordServiceImpl(
    BaseServiceImpl[NewWordMapper, NewWordModel], NewWordService
):
    """
    Implementation of the NewWordService interface.
    """

    def __init__(self, mapper: NewWordMapper):
        """
        Initialize the NewWordServiceImpl instance.

        Args:
            mapper (NewWordMapper): The NewWordMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper)
        self.mapper = mapper

    async def get_new_word(
        self,
        *,
        id: int,
    ) -> NewWordModel:
        new_word_record: NewWordModel = await self.mapper.select_by_id(id=id)
        if new_word_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return new_word_record

    async def list_new_words(
        self, req: ListNewWordsRequest
    ) -> tuple[list[NewWordModel], int]:
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
        if req.word is not None and req.word != "":
            filters[FilterOperators.EQ]["word"] = req.word
        if req.translation is not None and req.translation != "":
            filters[FilterOperators.EQ]["translation"] = req.translation
        if req.next_review_date is not None and req.next_review_date != "":
            filters[FilterOperators.EQ]["next_review_date"] = (
                req.next_review_date
            )
        if req.tenant is not None and req.tenant != "":
            filters[FilterOperators.EQ]["tenant"] = req.tenant
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
        self, *, parent_data: list[NewWordModel], schema_class: Type[NewWord]
    ) -> list[NewWord]:
        if not parent_data:
            return []
        new_word_list = [
            NewWord(**record.model_dump()) for record in parent_data
        ]
        return await self.mapper.get_children_recursively(
            parent_data=new_word_list, schema_class=schema_class
        )

    async def create_new_word(self, req: CreateNewWordRequest) -> NewWordModel:
        new_word: NewWordModel = NewWordModel(**req.new_word.model_dump())
        return await self.save(data=new_word)

    async def update_new_word(self, req: UpdateNewWordRequest) -> NewWordModel:
        new_word_record: NewWordModel = await self.retrieve_by_id(
            id=req.new_word.id
        )
        if new_word_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        new_word_model = NewWordModel(
            **req.new_word.model_dump(exclude_unset=True)
        )
        await self.modify_by_id(data=new_word_model)
        merged_data = {
            **new_word_record.model_dump(),
            **new_word_model.model_dump(),
        }
        return NewWordModel(**merged_data)

    async def delete_new_word(self, id: int) -> None:
        new_word_record: NewWordModel = await self.retrieve_by_id(id=id)
        if new_word_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_new_words(self, ids: list[int]) -> list[NewWordModel]:
        new_word_records = list[NewWordModel] = await self.retrieve_by_ids(
            ids=ids
        )
        if new_word_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(new_word_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in new_word_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(new_word_records)} != {str(not_exits_ids)}",
            )
        return new_word_records

    async def batch_create_new_words(
        self,
        *,
        req: BatchCreateNewWordsRequest,
    ) -> list[NewWordModel]:
        new_word_list: list[CreateNewWord] = req.new_words
        if not new_word_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [
            NewWordModel(**new_word.model_dump()) for new_word in new_word_list
        ]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_new_words(
        self, req: BatchUpdateNewWordsRequest
    ) -> list[NewWordModel]:
        new_word: BatchUpdateNewWord = req.new_word
        ids: list[int] = req.ids
        if not new_word or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=new_word.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_new_words(
        self, req: BatchPatchNewWordsRequest
    ) -> list[NewWordModel]:
        new_words: list[UpdateNewWord] = req.new_words
        if not new_words:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            new_word.model_dump(exclude_unset=True) for new_word in new_words
        ]
        await self.mapper.batch_update(items=update_data)
        new_word_ids: list[int] = [new_word.id for new_word in new_words]
        return await self.mapper.select_by_ids(ids=new_word_ids)

    async def batch_delete_new_words(self, req: BatchDeleteNewWordsRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_new_words_template(self) -> StreamingResponse:
        file_name = "new_word_import_tpl"
        return await excel_util.export_excel(
            schema=CreateNewWord, file_name=file_name
        )

    async def export_new_words(
        self, req: ExportNewWordsRequest
    ) -> StreamingResponse:
        ids: list[int] = req.ids
        new_word_list: list[NewWordModel] = await self.mapper.select_by_ids(
            ids=ids
        )
        if new_word_list is None or len(new_word_list) == 0:
            logger.error(f"No new_words found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        new_word_page_list = [
            ExportNewWord(**new_word.model_dump()) for new_word in new_word_list
        ]
        file_name = "new_word_data_export"
        return await excel_util.export_excel(
            schema=ExportNewWord,
            file_name=file_name,
            data_list=new_word_page_list,
        )

    async def import_new_words(
        self, req: ImportNewWordsRequest
    ) -> list[ImportNewWord]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        new_word_records = import_df.to_dict(orient="records")
        if new_word_records is None or len(new_word_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in new_word_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        new_word_import_list = []
        for new_word_record in new_word_records:
            try:
                new_word_create = ImportNewWord(**new_word_record)
                new_word_import_list.append(new_word_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in new_word_record.items()
                    if k in ImportNewWord.model_fields
                }
                new_word_create = ImportNewWord.model_construct(**valid_data)
                new_word_create.err_msg = ValidateService.get_validate_err_msg(
                    e
                )
                new_word_import_list.append(new_word_create)
                return new_word_import_list

        return new_word_import_list
