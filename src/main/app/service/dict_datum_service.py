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

from starlette.responses import StreamingResponse

from src.main.app.core.service.base_service import BaseService
from src.main.app.model.dict_datum_model import DictDatumModel
from src.main.app.schema.dict_datum_schema import (
    ListDictDataRequest,
    CreateDictDatumRequest,
    UpdateDictDatumRequest,
    BatchDeleteDictDataRequest,
    ExportDictDataRequest,
    BatchCreateDictDataRequest,
    BatchUpdateDictDataRequest,
    ImportDictDataRequest,
    ImportDictDatum,
    BatchPatchDictDataRequest,
)


class DictDatumService(BaseService[DictDatumModel], ABC):
    @abstractmethod
    async def get_dict_datum(
        self,
        *,
        id: int,
    ) -> DictDatumModel: ...

    @abstractmethod
    async def list_dict_data(
        self, *, req: ListDictDataRequest
    ) -> tuple[list[DictDatumModel], int]: ...

    @abstractmethod
    async def get_all_dict_data(self) -> list[DictDatumModel]: ...

    @abstractmethod
    async def get_dict_options(self, req: list[str]) -> list[DictDatumModel]: ...

    @abstractmethod
    async def create_dict_datum(self, *, req: CreateDictDatumRequest) -> DictDatumModel: ...

    @abstractmethod
    async def update_dict_datum(self, req: UpdateDictDatumRequest) -> DictDatumModel: ...

    @abstractmethod
    async def delete_dict_datum(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_dict_data(self, ids: list[int]) -> list[DictDatumModel]: ...

    @abstractmethod
    async def batch_create_dict_data(
        self,
        *,
        req: BatchCreateDictDataRequest,
    ) -> list[DictDatumModel]: ...

    @abstractmethod
    async def batch_update_dict_data(
        self, req: BatchUpdateDictDataRequest
    ) -> list[DictDatumModel]: ...

    @abstractmethod
    async def batch_patch_dict_data(
        self, req: BatchPatchDictDataRequest
    ) -> list[DictDatumModel]: ...

    @abstractmethod
    async def batch_delete_dict_data(self, req: BatchDeleteDictDataRequest): ...

    @abstractmethod
    async def export_dict_data_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_dict_data(self, req: ExportDictDataRequest) -> StreamingResponse: ...

    @abstractmethod
    async def import_dict_data(self, req: ImportDictDataRequest) -> list[ImportDictDatum]: ...
