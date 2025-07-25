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
from src.main.app.model.new_word_model import NewWordModel
from src.main.app.schema.new_word_schema import (
    ListNewWordsRequest,
    CreateNewWordRequest,
    NewWord,
    UpdateNewWordRequest,
    BatchDeleteNewWordsRequest,
    ExportNewWordsRequest,
    BatchCreateNewWordsRequest,
    BatchUpdateNewWordsRequest,
    ImportNewWordsRequest,
    ImportNewWord,
    BatchPatchNewWordsRequest,
)


class NewWordService(BaseService[NewWordModel], ABC):
    @abstractmethod
    async def get_new_word(
        self,
        *,
        id: int,
    ) -> NewWordModel: ...

    @abstractmethod
    async def list_new_words(
        self, *, req: ListNewWordsRequest
    ) -> tuple[list[NewWordModel], int]: ...

    @abstractmethod
    async def get_children_recursively(
        self, *, parent_data: list[NewWordModel], schema_class: Type[NewWord]
    ) -> list[NewWord]: ...

    @abstractmethod
    async def create_new_word(
        self, *, req: CreateNewWordRequest
    ) -> NewWordModel: ...

    @abstractmethod
    async def update_new_word(
        self, req: UpdateNewWordRequest
    ) -> NewWordModel: ...

    @abstractmethod
    async def delete_new_word(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_new_words(
        self, ids: list[int]
    ) -> list[NewWordModel]: ...

    @abstractmethod
    async def batch_create_new_words(
        self,
        *,
        req: BatchCreateNewWordsRequest,
    ) -> list[NewWordModel]: ...

    @abstractmethod
    async def batch_update_new_words(
        self, req: BatchUpdateNewWordsRequest
    ) -> list[NewWordModel]: ...

    @abstractmethod
    async def batch_patch_new_words(
        self, req: BatchPatchNewWordsRequest
    ) -> list[NewWordModel]: ...

    @abstractmethod
    async def batch_delete_new_words(self, req: BatchDeleteNewWordsRequest): ...

    @abstractmethod
    async def export_new_words_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_new_words(
        self, req: ExportNewWordsRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_new_words(
        self, req: ImportNewWordsRequest
    ) -> list[ImportNewWord]: ...
