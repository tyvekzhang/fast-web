"""GenTable domain service interface"""

from abc import ABC, abstractmethod

from src.main.app.model.gen_table_model import GenTableDO
from src.main.app.schema.gen_table_schema import (
    TableImport,
    GenTableQuery,
    GenTableDetail,
    GenTableExecute,
    GenTableRecord,
)
from src.main.app.core.service.base_service import BaseService


class GenTableService(BaseService[GenTableDO], ABC):
    @abstractmethod
    async def import_gen_table(self, table_import: TableImport): ...

    @abstractmethod
    async def preview_code(self, gen_table_id: int): ...

    @abstractmethod
    async def list_gen_tables(self, data: GenTableQuery): ...

    @abstractmethod
    async def download_code(self, table_id: int): ...

    @abstractmethod
    async def get_table_data(self, *, id: int, current: int, pageSize: int): ...

    @abstractmethod
    async def get_gen_table_detail(self, *, id: int) -> GenTableDetail: ...

    @abstractmethod
    async def modify_gen_table(
        self, gen_table_detail: GenTableDetail
    ) -> None: ...

    @abstractmethod
    async def execute_sql(
        self, gen_table_execute: GenTableExecute
    ) -> GenTableRecord: ...
