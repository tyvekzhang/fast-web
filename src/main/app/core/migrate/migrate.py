# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
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
"""Use when performing database migration"""

import importlib
from pathlib import Path
from typing import Optional

from loguru import logger

current_path = Path(__file__).resolve()
src_parent = None

for parent in current_path.parents:
    if parent.name == "src":
        src_parent = parent.parent
        break

if not src_parent:
    raise FileNotFoundError("Can not found src dir")

model_path = src_parent / "src" / "main" / "app" / "model"
codegen_path = src_parent / "src" / "main" / "app" / "model" / "codegen"

# List of directories to scan for model files
MODEL_PACKAGES = [
    model_path,
    codegen_path
]

def import_sql_models(packages: Optional[list[Path]] = None) -> dict[str, type]:
    packages_to_scan = packages or MODEL_PACKAGES
    imported_models = {}

    for package_dir in packages_to_scan:
        if not package_dir.exists():
            logger.warning(f"Package directory not found: {package_dir}")
            continue

        for model_file in package_dir.glob("*_model.py"):
            relative_path = model_file.relative_to(src_parent)
            module_path = ".".join(relative_path.with_suffix("").parts)

            try:
                module = importlib.import_module(module_path)
                for name in dir(module):
                    if name.endswith("Model"):
                        imported_models[name] = getattr(module, name)

            except ImportError as e:
                logger.error(f"Failed to import {module_path}: {e}")
            except Exception as e:
                logger.exception(f"Error processing {model_file}")

    return imported_models



# Import models from default packages
import_sql_models()

# Alternatively, import from specific packages:
# imported_models = import_models(["custom/package/models", "another/package/models"])

# For Alembic startup
ALEMBIC_START_SIGNAL = "Welcome! autogenerate is processing!"
