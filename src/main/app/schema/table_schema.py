"""Table domain schema"""

from typing import Optional, List

from pydantic import BaseModel

from src.main.app.schema.common_schema import PageBase
from src.main.app.schema.field_schema import FieldGenerate
from src.main.app.schema.index_schema import IndexGenerate


class TableAdd(BaseModel):
    database_id: int
    name: str
    comment: Optional[str] = None


class TableQuery(PageBase):
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
