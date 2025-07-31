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
"""Connection domain schema"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest


class ListConnectionsRequest(PaginationRequest):
    connection_name: Optional[str] = None
    database_type: Optional[str] = None


class Connection(BaseModel):
    id: int
    connection_name: str
    database_type: str
    connection_database: Optional[str] = None


class CreateConnection(BaseModel):
    connection_name: str
    database_type: str
    connection_database: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None


class ListConnectionResponse(BaseModel):
    id: int
    connection_name: str
    database_type: str
    host: str
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
