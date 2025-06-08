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
"""Project health probe"""

from fastapi import APIRouter

from src.main.app.core.schemas import HttpResponse

probe_router = APIRouter()


@probe_router.get("/liveness")
async def liveness() -> HttpResponse[str]:
    """
    Check if the system is alive.

    Returns:
        HttpResponse[str]: An HTTP response containing a success message
        with the string "Hi" as data.
    """
    return HttpResponse.success(msg="Hi")
