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
"""Offline API Documentation Setup Module"""

from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_redoc_html,
    get_swagger_ui_oauth2_redirect_html,
)
import os


def register_offline_openapi(app, resource_dir):
    """Register offline API documentation endpoints.

    Args:
        app: FastAPI application instance
        resource_dir: Base directory containing the 'static' folder with documentation assets

    Returns:
        None - modifies the app in place by adding documentation routes
    """
    # Setup offline openAPI documentation
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(resource_dir, "static")),
        name="static",
    )

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            swagger_favicon_url="/static/favicon.png",
            openapi_url=app.openapi_url,
            title=app.title,
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            redoc_favicon_url="/static/favicon.png",
            openapi_url=app.openapi_url,
            title=app.title,
            redoc_js_url="/static/redoc.standalone.js",
        )
