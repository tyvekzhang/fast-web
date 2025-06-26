# Copyright (c) 2025 Fast web and/or its affiliates. All rights reserved.
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
"""Async database session management using SQLAlchemy and SQLModel."""

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.main.app.core.config import config_manager

try:
    from sqlalchemy.ext.asyncio import async_sessionmaker
except ImportError:
    from sqlalchemy.orm import sessionmaker as async_sessionmaker


@asynccontextmanager
async def db_session(
    *, env: str = None, db_url: str = None, engine=None
) -> AsyncSession:
    """Creates a context with an open SQLAlchemy async session."""
    if engine is None:
        if db_url is None:
            db_url = config_manager.get_database_url(env=env)
        engine = create_async_engine(db_url, echo=True)
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, autocommit=False, autoflush=True
    )
    async with async_session() as session:
        yield session
    await engine.dispose()
