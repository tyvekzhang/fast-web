"""Menu Service"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from src.main.app.core.service.base_service import BaseService
from src.main.app.model.menus_model import MenuModel
from src.main.app.schema.menus_schema import (
    ListMenusRequest,
    CreateMenuRequest,
    Menu,
    UpdateMenuRequest,
    BatchDeleteMenusRequest,
    ExportMenusRequest,
    BatchCreateMenusRequest,
    BatchUpdateMenusRequest,
    ImportMenusRequest,
    ImportMenu,
    BatchPatchMenusRequest,
)


class MenuService(BaseService[MenuModel], ABC):
    @abstractmethod
    async def get_menu(
        self,
        *,
        id: int,
    ) -> MenuModel: ...

    @abstractmethod
    async def list_menus(
        self, *, req: ListMenusRequest
    ) -> tuple[list[MenuModel], int]: ...

    @abstractmethod
    async def get_children_recursively(
        self, *, parent_data: list[MenuModel], schema_class: Type[Menu]
    ) -> list[Menu]: ...

    @abstractmethod
    async def create_menu(self, *, req: CreateMenuRequest) -> MenuModel: ...

    @abstractmethod
    async def update_menu(self, req: UpdateMenuRequest) -> MenuModel: ...

    @abstractmethod
    async def delete_menu(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_menus(self, ids: list[int]) -> list[MenuModel]: ...

    @abstractmethod
    async def batch_create_menus(
        self,
        *,
        req: BatchCreateMenusRequest,
    ) -> list[MenuModel]: ...

    @abstractmethod
    async def batch_update_menus(
        self, req: BatchUpdateMenusRequest
    ) -> list[MenuModel]: ...

    @abstractmethod
    async def batch_patch_menus(
        self, req: BatchPatchMenusRequest
    ) -> list[MenuModel]: ...

    @abstractmethod
    async def batch_delete_menus(self, req: BatchDeleteMenusRequest): ...

    @abstractmethod
    async def export_menus_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_menus(
        self, req: ExportMenusRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_menus(
        self, req: ImportMenusRequest
    ) -> list[ImportMenu]: ...
