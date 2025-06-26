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
