"""DictData schema"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.app.core.schema import BasePage


class DictDataPage(BaseModel):
    """
    字典数据分页信息
    """

    # 主键
    id: int
    # 字典排序
    sort: Optional[int] = None
    # 字典标签
    label: Optional[str] = None
    # 字典键值
    value: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 回显样式
    echo_style: Optional[str] = None
    # 扩展样式
    ext_class: Optional[str] = None
    # 是否默认(1是 0否)
    is_default: Optional[int] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None


class DictDataQuery(BasePage):
    """
    字典数据查询参数
    """

    # 主键
    id: Optional[int] = None
    # 字典排序
    sort: Optional[int] = None
    # 字典标签
    label: Optional[str] = None
    # 字典键值
    value: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 回显样式
    echo_style: Optional[str] = None
    # 扩展样式
    ext_class: Optional[str] = None
    # 是否默认(1是 0否)
    is_default: Optional[int] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 创建时间
    create_time: Optional[datetime] = None
    sort: Optional[str] = None


class DictDataCreate(BaseModel):
    """
    字典数据新增
    """

    # 字典排序
    sort: Optional[int] = None
    # 字典标签
    label: Optional[str] = None
    # 字典键值
    value: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 回显样式
    echo_style: Optional[str] = None
    # 扩展样式
    ext_class: Optional[str] = None
    # 是否默认(1是 0否)
    is_default: Optional[int] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None
    # 错误信息
    err_msg: Optional[str] = Field(None, alias="errMsg")


class DictDataModify(BaseModel):
    """
    字典数据更新
    """

    # 主键
    id: int
    # 字典排序
    sort: Optional[int] = None
    # 字典标签
    label: Optional[str] = None
    # 字典键值
    value: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 回显样式
    echo_style: Optional[str] = None
    # 扩展样式
    ext_class: Optional[str] = None
    # 是否默认(1是 0否)
    is_default: Optional[int] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None


class DictDataBatchModify(BaseModel):
    """
    字典数据批量更新
    """

    ids: List[int]
    # 字典排序
    sort: Optional[int] = None
    # 字典标签
    label: Optional[str] = None
    # 字典键值
    value: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 回显样式
    echo_style: Optional[str] = None
    # 扩展样式
    ext_class: Optional[str] = None
    # 是否默认(1是 0否)
    is_default: Optional[int] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None


class DictDataDetail(BaseModel):
    """
    字典数据详情
    """

    # 主键
    id: int
    # 字典排序
    sort: Optional[int] = None
    # 字典标签
    label: Optional[str] = None
    # 字典键值
    value: Optional[str] = None
    # 字典类型
    type: Optional[str] = None
    # 回显样式
    echo_style: Optional[str] = None
    # 扩展样式
    ext_class: Optional[str] = None
    # 是否默认(1是 0否)
    is_default: Optional[int] = None
    # 状态(1正常 0停用)
    status: Optional[int] = None
    # 备注
    comment: Optional[str] = None
    # 创建时间
    create_time: Optional[datetime] = None
