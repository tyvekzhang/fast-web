"""Template operation util"""

import os
from typing import Any
from jinja2 import Template
from src.main.app.core.utils.work_path_util import resource_dir

home_template_dir: str = os.path.join(resource_dir, "template")


def load_template_file(template_name: str) -> Template:
    """
    Load template.

    Args:
        template_name: Name of the template file.

    Returns:
        Jinja2 Template object.

    Raises:
        SystemException: If template not found.
    """
    template_path: str = os.path.join(home_template_dir, template_name)
    if not os.path.exists(template_path):
        pass
    with open(template_path, "r", encoding="UTF-8") as f:
        return Template(f.read())


def render_template(template: Template, **context: Any) -> str:
    """
    Render template.

    Args:
        template: Template to render.
        **context: Template variables.

    Returns:
        Rendered template string.
    """
    return template.render(**context)


def load_and_render_template(template_name: str, **context: Any) -> str:
    """
    Load and render template.

    Args:
        template_name: Name of the template file.
        **context: Template variables for rendering.

    Returns:
        Rendered template string.

    Raises:
        SystemException: If template not found or rendering fails.
    """
    return render_template(load_template_file(template_name), **context)
