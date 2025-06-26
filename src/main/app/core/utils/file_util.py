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
"""Path utility functions for locating project directories and files."""

import os
from pathlib import Path


def get_utils_dir() -> str:
    """Get the absolute path of the directory containing this utils module."""
    return os.path.dirname(os.path.abspath(__file__))


def get_resource_dir() -> str:
    """Get the absolute path of the project's resource directory (3 levels up from utils)."""
    utils_dir = get_utils_dir()
    return os.path.abspath(
        os.path.join(utils_dir, os.pardir, os.pardir, os.pardir, "resource")
    )


def _find_marker_path(marker_file: str, return_dir: bool = True) -> str:
    """
    Internal helper to locate marker file or its parent directory by searching upwards.

    Args:
        marker_file: Filename to search for
        return_dir: If True returns parent directory, False returns file path

    Returns:
        Requested absolute path (dir or file)

    Raises:
        FileNotFoundError: If marker file not found
    """
    current = Path(__file__).resolve().parent
    while True:
        target = current / marker_file
        if target.exists():
            return str(current if return_dir else target.absolute())

        parent = current.parent
        if parent == current:
            raise FileNotFoundError(f"Marker file not found: {marker_file}")
        current = parent


def get_file_dir(marker_file: str) -> str:
    """Locate directory containing the specified marker file.

    See _find_marker_path docstring for details.
    """
    return _find_marker_path(marker_file, return_dir=True)


def get_file_path(marker_file: str) -> str:
    """Locate the absolute path of the specified marker file.

    See _find_marker_path docstring for details.
    """
    return _find_marker_path(marker_file, return_dir=False)
