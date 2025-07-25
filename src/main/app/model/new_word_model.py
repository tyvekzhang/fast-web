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
"""NewWord data model"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    DateTime,
    BigInteger,
    String,
    Integer,
)
from src.main.app.core.utils.snowflake_util import snowflake_id


class NewWordBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,
    )
    word: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            default=None,
        )
    )
    translation: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            default=None,
        )
    )
    next_review_date: Optional[str] = Field(
        sa_column=Column(
            String,
            nullable=True,
            default=None,
        )
    )
    tenant: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
        )
    )
    update_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "onupdate": datetime.utcnow,
        },
    )


class NewWordModel(NewWordBase, table=True):
    __tablename__ = "read_new_word"
    __table_args__ = ()
