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
"""FastAPI Request Logging Middleware"""

import time
import uuid

from loguru import logger
from fastapi import Request


async def log_requests(request: Request, call_next):
    """Middleware to log all incoming requests and responses"""
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # Log request start information
    start_time = time.time()

    # Request started log
    logger.info(
        f"Request started - {request.method} {request.url.path} "
        f"(ID: {request_id}, IP: {request.client.host if request.client else None}, "
        f"UA: {request.headers.get('user-agent')})"
    )

    try:
        response = await call_next(request)
    except Exception as exc:
        # Log exception information
        logger.error(
            f"Request failed - {request.method} {request.url.path} "
            f"(ID: {request_id}, Error: {str(exc)})",
            exc_info=True,
        )
        raise

    # Calculate processing time
    process_time = round((time.time() - start_time) * 1000, 2)

    # Request completed log
    logger.info(
        f"Request completed - {request.method} {request.url.path} "
        f"(ID: {request_id}, Status: {response.status_code}, "
        f"Time: {process_time}ms)"
    )

    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id
    return response
