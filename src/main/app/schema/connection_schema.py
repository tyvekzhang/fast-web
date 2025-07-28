"""Connection domain schema"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.main.app.core.schema import PaginationRequest


class ConnectionAdd(BaseModel):
    connection_name: str
    database_type: str
    connection_database: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None


class ConnectionQuery(PaginationRequest):
    pass


class ConnectionQueryResponse(BaseModel):
    id: int
    connection_name: str
    database_type: str
    host: str
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None


class ConnectionExport(BaseModel):
    pass


class ConnectionQueryForm(BaseModel):
    pass


class ConnectionModify(BaseModel):
    pass
