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
"""Index domain schema"""

from typing import Optional

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest


class IndexAdd(BaseModel):
    pass


class IndexQuery(PaginationRequest):
    table_id: int


class IndexExport(BaseModel):
    pass


class IndexQueryForm(BaseModel):
    pass


class IndexModify(BaseModel):
    pass


class IndexGenerate(BaseModel):
    name: str
    field: str
    type: Optional[str] = "normal"
    remark: Optional[str] = None
