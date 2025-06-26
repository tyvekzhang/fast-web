"""Project enumeration information"""

from enum import Enum


class UserStatusEnum(Enum):
    """User Status Enum"""

    DISABLED = (0, "停用")
    PENDING = (1, "待审核")
    ACTIVE = (2, "正常")
    DELETED = (3, "已注销")

    def __init__(self, code, status):
        self.code = code
        self.status = status

    @classmethod
    def get_by_code(cls, code):
        for item in cls:
            if item.code == code:
                return item
        raise ValueError(f"Invalid status code: {code}")

    @classmethod
    def get_status_by_code(cls, code):
        for item in cls:
            if item.code == code:
                return item.status
        raise ValueError(f"Invalid status code: {code}")
