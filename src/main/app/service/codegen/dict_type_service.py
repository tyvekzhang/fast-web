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
"""Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from src.main.app.core.service.base_service import BaseService
from src.main.app.model.codegen.dict_type_model import DictTypeModel
from src.main.app.schema.codegen.dict_type_schema import (
    ListDictTypesRequest,
    CreateDictTypeRequest,
    DictType,
    UpdateDictTypeRequest,
    BatchDeleteDictTypesRequest,
    ExportDictTypesRequest,
    BatchCreateDictTypesRequest,
    BatchUpdateDictTypesRequest,
    ImportDictTypesRequest,
    ImportDictType,
    BatchPatchDictTypesRequest,
)


class DictTypeService(BaseService[DictTypeModel], ABC):
    @abstractmethod
    async def get_dict_type(
        self,
        *,
        id: int,
    ) -> DictTypeModel: ...

    @abstractmethod
    async def list_dict_types(
        self, *, req: ListDictTypesRequest
    ) -> tuple[list[DictTypeModel], int]: ...

    @abstractmethod
    async def get_children_recursively(
        self, *, parent_data: list[DictTypeModel], schema_class: Type[DictType]
    ) -> list[DictType]: ...

    @abstractmethod
    async def create_dict_type(self, *, req: CreateDictTypeRequest) -> DictTypeModel: ...

    @abstractmethod
    async def update_dict_type(self, req: UpdateDictTypeRequest) -> DictTypeModel: ...

    @abstractmethod
    async def delete_dict_type(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_dict_types(self, ids: list[int]) -> list[DictTypeModel]: ...

    @abstractmethod
    async def batch_create_dict_types(
        self,
        *,
        req: BatchCreateDictTypesRequest,
    ) -> list[DictTypeModel]: ...

    @abstractmethod
    async def batch_update_dict_types(
        self, req: BatchUpdateDictTypesRequest
    ) -> list[DictTypeModel]: ...

    @abstractmethod
    async def batch_patch_dict_types(
        self, req: BatchPatchDictTypesRequest
    ) -> list[DictTypeModel]: ...

    @abstractmethod
    async def batch_delete_dict_types(self, req: BatchDeleteDictTypesRequest): ...

    @abstractmethod
    async def export_dict_types_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_dict_types(self, req: ExportDictTypesRequest) -> StreamingResponse: ...

    @abstractmethod
    async def import_dict_types(self, req: ImportDictTypesRequest) -> list[ImportDictType]: ...
