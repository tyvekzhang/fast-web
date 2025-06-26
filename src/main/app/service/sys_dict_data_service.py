"""DictData Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import UploadFile
from starlette.responses import StreamingResponse
from src.main.app.model.sys_dict_data_model import DictDataModel
from src.main.app.core.schema import PageResult, CurrentUser
from src.main.app.schema.sys_dict_data_schema import (
    DictDataQuery,
    DictDataDetail,
    DictDataCreate,
)
from src.main.app.core.service.base_service import BaseService


class DictDataService(BaseService[DictDataModel], ABC):
    @abstractmethod
    async def get_dict_data_by_page(
        self, *, dict_data_query: DictDataQuery, current_user: CurrentUser
    ) -> PageResult: ...

    @abstractmethod
    async def get_dict_data_detail(
        self, *, id: int, current_user: CurrentUser
    ) -> Optional[DictDataDetail]: ...

    @abstractmethod
    async def export_dict_data_page(
        self, *, ids: List[int], current_user: CurrentUser
    ) -> Optional[StreamingResponse]: ...

    @abstractmethod
    async def create_dict_data(
        self, *, dict_data_create: DictDataCreate, current_user: CurrentUser
    ) -> DictDataModel: ...

    @abstractmethod
    async def batch_create_dict_data(
        self,
        *,
        dict_data_create_list: List[DictDataCreate],
        current_user: CurrentUser,
    ) -> List[int]: ...

    @abstractmethod
    async def import_dict_data(
        self, *, file: UploadFile, current_user: CurrentUser
    ) -> List[DictDataCreate]: ...
