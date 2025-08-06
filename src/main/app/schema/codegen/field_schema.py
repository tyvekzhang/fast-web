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
"""Field main schema"""
from typing import Optional

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest
from src.main.app.model.codegen.field_model import FieldModel
from src.main.app.model.codegen.meta_field_model import MetaFieldModel


class FieldResponse(BaseModel):
    id: int
    field_name: str
    comment: Optional[str] = None


class GenTableColumnAdd(BaseModel):
    pass


class GenTableColumnQuery(PaginationRequest):
    pass


class GenTableColumnQueryResponse(BaseModel):
    pass


class GenTableColumnExport(BaseModel):
    pass


class GenTableColumnQueryForm(BaseModel):
    pass


class GenTableColumnModify(BaseModel):
    pass


class GenField(BaseModel):
    meta_field: MetaFieldModel
    field: FieldModel


class GenFieldDb(BaseModel):
    gen_field: FieldModel
    db_field: MetaFieldModel
