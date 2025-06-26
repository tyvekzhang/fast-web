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
"""Main entry point of the application."""

import os
import sys
import argparse
from pathlib import Path

import uvicorn
from loguru import logger


def find_project_root(marker_file: str = "pyproject.toml") -> Path:
    """Locate the project root directory by searching for a marker file.

    Args:
        marker_file: File name that identifies the project root.

    Returns:
        Path to the project root directory.

    Raises:
        FileNotFoundError: If marker file is not found in any parent directory.
    """
    current_dir = Path(__file__).resolve().parent

    while True:
        if (current_dir / marker_file).exists():
            return current_dir

        parent_dir = current_dir.parent

        if parent_dir == current_dir:
            raise FileNotFoundError(
                f"Could not find {marker_file} in any parent directory"
            )

        current_dir = parent_dir


def parse_arguments() -> argparse.Namespace:
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fast web server with custom configurations"
    )

    parser.add_argument(
        "-e",
        "--env",
        type=str,
        choices=["dev", "test", "prod"],  # Add expected environments
        default="dev",
        help="Specify the runtime environment (dev|test|prod)",
    )
    parser.add_argument(
        "-c",
        "--config-file",
        type=str,
        default=None,
        help="Path to a custom configuration file",
    )

    return parser.parse_args()


def configure_environment(args: argparse.Namespace) -> None:
    """Set up environment variables based on command line arguments."""
    from src.main.app.core import constant

    os.environ[constant.ENV] = args.env
    if args.config_file:
        os.environ[constant.CONFIG_FILE] = args.config_file


def run_server() -> None:
    """Load configuration and start the Uvicorn server."""
    from src.main.app.core.config import config_manager

    server_config = config_manager.load_server_config()
    logger.info(
        f"OpenAPI url: http://{server_config.host}:{server_config.port}/docs"
    )
    uvicorn.run(
        app="src.main.app.server:app",
        host=server_config.host,
        port=server_config.port,
        workers=server_config.workers,
    )


def main() -> None:
    """Main application entry point."""
    project_root = find_project_root()
    sys.path.insert(0, str(project_root))

    args = parse_arguments()
    configure_environment(args)
    run_server()


if __name__ == "__main__":
    main()
