"""Use when performing database migration"""

import importlib
import os
from pathlib import Path
from typing import Optional
from loguru import logger

# List of directories to scan for model files
MODEL_PACKAGES = [
    "src/main/app/model",
]


def import_sql_models(
    packages: Optional[list[str]] = None,
) -> None:
    """Dynamically import all model classes from specified packages.

    Scans for Python files matching '*_model.py' pattern in each package directory.
    Model classes are identified by names ending with 'Model'.

    Args:
        packages: List of package paths to search. If None, uses default MODEL_PACKAGES.

    Returns:
        Dictionary mapping class names to class objects for all imported models.
    """
    packages_to_scan = packages or MODEL_PACKAGES

    for package_path in packages_to_scan:
        package_dir = Path(package_path)

        if not package_dir.exists():
            logger.warning(f"Package directory not found: {package_dir}")
            continue

        for model_file in package_dir.glob("*_model.py"):
            try:
                # Convert path to module import format (e.g., "src/main/app/models/file_model")
                module_path = (
                    str(model_file.with_suffix(""))
                    .replace("/", ".")
                    .replace(os.sep, ".")
                )
                module = importlib.import_module(module_path)

                for name in dir(module):
                    if name.endswith("Model"):
                        globals()[name] = getattr(module, name)

            except Exception as e:
                logger.error(f"Unexpected error processing {model_file}: {e}")


# Import models from default packages
import_sql_models()

# Alternatively, import from specific packages:
# imported_models = import_models(["custom/package/models", "another/package/models"])

# For Alembic startup
ALEMBIC_START_SIGNAL = "Welcome! autogenerate is processing!"
