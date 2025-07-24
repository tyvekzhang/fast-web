# Copyright (c) 2025 Admin and/or its affiliates. All rights reserved.
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
"""DbDatabase data model"""

from datetime import datetime
from typing import Optional
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    Index,
    BigInteger,
    String,
    DateTime,
    Integer,
)
from src.main.app.core.utils.snowflake_util import snowflake_id


class DbDatabaseBase(SQLModel):
    id: int = Field(
        default_factory=snowflake_id,
        primary_key=True,
        nullable=False,
        sa_type=BigInteger,
    )
    connection_id: int = Field(
        sa_column=Column(
            Integer,
            nullable=False,
            default=None,
        )
    )
    database_name: str = Field(
        sa_column=Column(
            String(64),
            nullable=False,
            default=None,
        )
    )
    owner: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
        )
    )
    template: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
        )
    )
    encoding: Optional[str] = Field(
        sa_column=Column(
            String(32),
            nullable=True,
            default=None,
        )
    )
    collation_order: Optional[str] = Field(
        sa_column=Column(
            String(32),
            nullable=True,
            default=None,
        )
    )
    character_classification: Optional[str] = Field(
        sa_column=Column(
            String(32),
            nullable=True,
            default=None,
        )
    )
    tablespace: Optional[str] = Field(
        sa_column=Column(
            String(64),
            nullable=True,
            default=None,
        )
    )
    connection_limit: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
        )
    )
    allow_connection: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
        )
    )
    is_template: Optional[int] = Field(
        sa_column=Column(
            Integer,
            nullable=True,
            default=None,
        )
    )
    create_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
    )
    update_time: Optional[datetime] = Field(
        sa_type=DateTime,
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "onupdate": datetime.utcnow,
        },
    )


class DbDatabaseModel(DbDatabaseBase, table=True):
    __tablename__ = "db_database"
    __table_args__ = (Index("ix_db_database_connection_id", "connection_id"),)
