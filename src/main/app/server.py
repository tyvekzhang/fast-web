"""
Server startup that include register router、session、cors、global exception
handler、jwt, openapi...
"""

import os
import subprocess
import time
from pathlib import Path

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from src.main.app.core import exception
from src.main.app.core.config import config_manager
from src.main.app.core.constant import RESOURCE_DIR
from src.main.app.core.middleware.db_session_middleware import (
    SQLAlchemyMiddleware,
)
from src.main.app.core.middleware.jwt_middleware import jwt_middleware
from src.main.app.core.openapi import offline
from src.main.app.core.session.db_engine import get_async_engine
from src.main.app.core import router

# Load config
server_config = config_manager.load_server_config()
security_config = config_manager.load_security_config()


# Setup timezone
if os.name == "nt":
    subprocess.run(["tzutil", "/s", server_config.win_tz], check=True)

else:
    os.environ["TZ"] = server_config.linux_tz
    time.tzset()

# Setup log
logger.add(
    server_config.log_file_path,
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG" if server_config.debug else "INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# Setup fastapi instance
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title=server_config.name,
    version=server_config.version,
    description=server_config.app_desc,
)

# Register middleware
app.add_middleware(SQLAlchemyMiddleware, custom_engine=get_async_engine())
origins = [
    origin.strip() for origin in security_config.backend_cors_origins.split(",")
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(jwt_middleware)

# Register exception handler
exception.register_exception_handlers(app)

# Setup router
current_dir = Path(__file__).parent.absolute()
controller_path = os.path.join(current_dir, "controller")
app.include_router(
    router.register_router([controller_path]),
    prefix=server_config.api_prefix,
)

# Register offline openapi
offline.register_offline_openapi(app=app, resource_dir=RESOURCE_DIR)
