"""Load and render the file templates shipped with FastForge."""

from collections.abc import Mapping
from functools import lru_cache
from importlib.resources import files
from pathlib import PurePosixPath

TEMPLATE_PACKAGE_DIR = "template_files"


@lru_cache
def load_template(template_name: str) -> str:
    """Load a template from the installed ``forge`` package."""
    relative_path = PurePosixPath(template_name)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError(f"Unsafe template path: {template_name}")

    template = files("forge").joinpath(TEMPLATE_PACKAGE_DIR, *relative_path.parts)
    if not template.is_file():
        raise FileNotFoundError(f"Template not found: {template_name}")
    return template.read_text(encoding="utf-8")


def render_template(template_name: str, context: Mapping[str, object]) -> str:
    """Render a packaged template with the supplied context."""
    template = load_template(template_name)
    try:
        return template.format_map(context)
    except (KeyError, IndexError, ValueError) as exc:
        raise RuntimeError(f"Error formatting template '{template_name}': {exc}") from exc
