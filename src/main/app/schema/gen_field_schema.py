"""GenTableColumn domain schema"""

from pydantic import BaseModel

from src.main.app.model.db_field_model import FieldDO
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.schema.common_schema import PageBase


class GenTableColumnAdd(BaseModel):
    pass


class GenTableColumnQuery(PageBase):
    pass


class GenTableColumnQueryResponse(BaseModel):
    pass


class GenTableColumnExport(BaseModel):
    pass


class GenTableColumnQueryForm(BaseModel):
    pass


class GenTableColumnModify(BaseModel):
    pass


class FieldGen(BaseModel):
    #
    field: FieldDO
    gen_field: GenFieldDO


class GenFieldDb(BaseModel):
    gen_field: GenFieldDO
    db_field: FieldDO
