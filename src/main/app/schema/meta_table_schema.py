"""Table domain schema"""

from typing import Optional, List

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest
from src.main.app.schema.index_schema import IndexGenerate
from src.main.app.schema.meta_field_schema import FieldGenerate


class TableAdd(BaseModel):
    database_id: int
    name: str
    comment: Optional[str] = None


class TableQuery(PaginationRequest):
    database_id: int


class TableGenerate(BaseModel):
    database_id: int
    table_name: str
    class_name: Optional[str] = None
    comment: Optional[str] = None
    field_metadata: List[FieldGenerate]
    index_metadata: List[IndexGenerate]


class TableExport(BaseModel):
    pass


class TableQueryForm(BaseModel):
    pass


class TableModify(BaseModel):
    pass
