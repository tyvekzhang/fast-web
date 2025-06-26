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
