"""Routing of the application.

Automatically discovers and includes all controller routers from the controller directory.
Each controller file should be named '*_controller.py' and contain a corresponding '*_router' variable."""

import importlib
import os
from pathlib import Path

from fastapi import APIRouter
from loguru import logger


def register_router(
    controller_dirs=None,
    controller_flag="controller",
    router_flag="router",
    remove_prefix_set=None,
) -> APIRouter:
    if controller_dirs is None:
        controller_dirs = []
    if remove_prefix_set is None:
        remove_prefix_set = ["sys"]
    router = APIRouter()

    for controller_item in controller_dirs:
        controller_dir = Path(controller_item).resolve()
        for controller_file in controller_dir.glob(f"*_{controller_flag}.py"):
            module_name = controller_file.stem
            controller_item_str = str(controller_item)
            relative_path = controller_item_str.split("src")[1]
            module_path = f"src{relative_path}.{module_name}".replace(
                "/", "."
            ).replace(os.sep, ".")

            try:
                module = importlib.import_module(module_path)
                router_var_name = module_name.replace(
                    controller_flag, router_flag
                )
                for remove_prefix in remove_prefix_set:
                    router_var_name = router_var_name.replace(
                        f"{remove_prefix}_", ""
                    )

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
                        tags=[module_name.replace(f"_{controller_flag}", "")],
                        prefix=prefix,
                    )
            except ImportError as e:
                logger.error(f"Failed to import {module_path}: {e}")
                raise SystemError(f"Failed to import {module_path}: {e}")

    return router
