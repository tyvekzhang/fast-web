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
"""NewWord schema"""

from __future__ import annotations
from fastapi import UploadFile
from typing import Optional
from pydantic import BaseModel, Field
from src.main.app.core.schema import PaginationRequest


class ListNewWordsRequest(PaginationRequest):
    id: Optional[int] = None
    word: Optional[str] = None
    translation: Optional[str] = None
    next_review_date: Optional[str] = None
    tenant: Optional[int] = None


class NewWord(BaseModel):
    id: Optional[int] = None
    word: Optional[str] = None
    translation: Optional[str] = None
    next_review_date: Optional[str] = None
    tenant: Optional[int] = None


class NewWordDetail(BaseModel):
    id: Optional[int] = None
    word: Optional[str] = None
    translation: Optional[str] = None
    next_review_date: Optional[str] = None
    tenant: Optional[int] = None


class CreateNewWord(BaseModel):
    word: Optional[str] = None
    translation: Optional[str] = None
    next_review_date: Optional[str] = None
    tenant: Optional[int] = None


class CreateNewWordRequest(BaseModel):
    new_word: CreateNewWord = Field(..., alias="newWord")


class UpdateNewWord(BaseModel):
    id: Optional[int] = None
    word: Optional[str] = None
    translation: Optional[str] = None
    next_review_date: Optional[str] = None
    tenant: Optional[int] = None


class UpdateNewWordRequest(BaseModel):
    new_word: UpdateNewWord


class BatchGetNewWordsResponse(BaseModel):
    new_words: list[NewWordDetail]


class BatchCreateNewWordsRequest(BaseModel):
    new_words: list[CreateNewWord]


class BatchCreateNewWordsResponse(BaseModel):
    new_words: list[NewWord]


class BatchUpdateNewWord(BaseModel):
    word: Optional[str] = None
    translation: Optional[str] = None
    next_review_date: Optional[str] = None
    tenant: Optional[int] = None


class BatchUpdateNewWordsRequest(BaseModel):
    ids: list[int]
    new_word: BatchUpdateNewWord


class BatchPatchNewWordsRequest(BaseModel):
    new_words: list[UpdateNewWord]


class BatchUpdateNewWordsResponse(BaseModel):
    new_words: list[NewWord]


class BatchDeleteNewWordsRequest(BaseModel):
    ids: list[int]


class ExportNewWord(NewWord):
    pass


class ExportNewWordsRequest(BaseModel):
    ids: list[int]


class ImportNewWordsRequest(BaseModel):
    file: UploadFile


class ImportNewWord(CreateNewWord):
    err_msg: Optional[str] = Field(None, alias="errMsg")


class ImportNewWordsResponse(BaseModel):
    new_words: list[ImportNewWord]
