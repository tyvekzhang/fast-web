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
"""Common constant"""

import os

current_dir: str = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR: str = os.path.abspath(
    os.path.join(current_dir, os.pardir, os.pardir, os.pardir, "resource")
)
ENV = "env"
CONFIG_FILE = "config_file"
AUTHORIZATION = "Authorization"
CONFIG_FILE_NAME = "config.yml"
MAX_PAGE_SIZE = 1000
ROOT_PARENT_ID = 0
PARENT_ID = "parent_id"


class FilterOperators:
    EQ = "EQ"
    NE = "NE"
    GT = "GT"
    GE = "GE"
    LT = "LT"
    LE = "LE"
    BETWEEN = "BETWEEN"
    LIKE = "LIKE"
