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
