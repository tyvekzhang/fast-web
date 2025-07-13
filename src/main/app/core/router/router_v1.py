"""Routing of the application.

Automatically discovers and includes all controller routers from the controller directory.
Each controller file should be named '*_controller.py' and contain a corresponding '*_router' variable.
"""

import importlib
import os
from pathlib import Path

from fastapi import APIRouter
from loguru import logger

from src.main.app.core.utils import string_util

# Constants
DEFAULT_API_VERSION = "/v1"
DEFAULT_CONTROLLER_FLAG = "controller"
DEFAULT_ROUTER_FLAG = "router"
DEFAULT_REMOVE_PREFIX_SET = {"sys"}
CONTROLLER_FILE_PATTERN_TEMPLATE = "*_{}.py"
MODULE_BASE_PREFIX = "src"
MODULE_SEPARATOR = "."


def register_router(
    controller_dirs=None,
    controller_flag=DEFAULT_CONTROLLER_FLAG,
    router_flag=DEFAULT_ROUTER_FLAG,
    remove_prefix_set=None,
    api_version=DEFAULT_API_VERSION,
) -> APIRouter:
    if controller_dirs is None:
        controller_dirs = []
    if remove_prefix_set is None:
        remove_prefix_set = DEFAULT_REMOVE_PREFIX_SET

    router = APIRouter()

    for controller_item in controller_dirs:
        controller_dir = Path(controller_item).resolve()
        for controller_file in controller_dir.glob(CONTROLLER_FILE_PATTERN_TEMPLATE.format(controller_flag)):
            module_name = controller_file.stem
            controller_item_str = str(controller_item)
            relative_path = controller_item_str.split(MODULE_BASE_PREFIX)[1]
            module_path = f"{MODULE_BASE_PREFIX}{relative_path}.{module_name}".replace(
                "/", MODULE_SEPARATOR
            ).replace(os.sep, MODULE_SEPARATOR)

            try:
                module = importlib.import_module(module_path)
                router_var_name = module_name.replace(controller_flag, router_flag)
                for remove_prefix in remove_prefix_set:
                    router_var_name = router_var_name.replace(f"{remove_prefix}_", "")

                if hasattr(module, router_var_name):
                    prefix = (
                        f"/{module_name.replace(f'_{controller_flag}', '')}"
                    )
                    for remove_prefix in remove_prefix_set:
                        prefix = prefix.replace(
                            f"{remove_prefix}_", ""
                        ).replace("_", "-")
                    router_instance = getattr(module, router_var_name)
                    router.include_router(
                        router_instance,
                        tags=[string_util.snake_to_title(module_name.replace(f"_{controller_flag}", ""))],
                        prefix=f"{api_version}{prefix}",
                    )
            except ImportError as e:
                logger.error(f"Failed to import {module_path}: {e}")
                raise SystemError(f"Failed to import {module_path}: {e}")

    return router
