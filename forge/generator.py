"""
Module generator — scaffolds Clean Architecture modules for FastAPI.
"""

import keyword
from pathlib import Path
from typing import Any

from forge.templates import render_template


def normalize_module_name(name: str) -> str:
    """Normalize a user-provided module name."""
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def validate_module_name(name: str) -> str:
    """Return a safe Python module name or raise ``ValueError``."""
    normalized_name = normalize_module_name(name)
    if not normalized_name.isidentifier() or keyword.iskeyword(normalized_name):
        raise ValueError(f"'{normalized_name}' is not a valid Python module name.")
    return normalized_name


def resolve_module_path(module_name: str, target_dir: str | Path) -> Path:
    """Resolve a module path and guarantee it is a direct child of target_dir."""
    safe_name = validate_module_name(module_name)
    target_path = Path(target_dir).resolve()
    module_path = (target_path / safe_name).resolve()
    if module_path.parent != target_path:
        raise ValueError(f"Module path escapes target directory: {module_path}")
    return module_path


def to_pascal_case(name: str) -> str:
    """Convert snake_case or kebab-case to PascalCase."""
    return "".join(word.capitalize() for word in name.replace("-", "_").split("_"))


def create_module(module_name: str, target_dir: str | Path = "src/modules") -> Path:
    """
    Generate a full Clean Architecture module.

    Args:
        module_name: Name of the module (e.g., "telegram", "offers").
        target_dir: Parent directory where the module will be created.

    Returns:
        Path to the generated module directory.

    Raises:
        FileExistsError: If the module directory already exists.
    """
    module_name = validate_module_name(module_name)
    module_path = resolve_module_path(module_name, target_dir)
    entity_name = to_pascal_case(module_name)
    context = {
        "module_name": module_name,
        "ModuleName": entity_name,
        "entity_name": entity_name,
        "use_case_name": f"create_{module_name}",
    }

    if module_path.exists():
        raise FileExistsError(f"Module '{module_name}' already exists at {module_path}")

    _create_structure(module_path, context)
    _register_module(module_name, target_dir)

    return module_path


def _create_structure(base_path: Path, context: dict[str, Any]) -> None:
    """Create the directory tree and write template files."""
    structure: list[tuple[str, str | None]] = [
        # Module root
        ("__init__.py", "module/__init__.py.tpl"),
        ("README.md", "module/README.md.tpl"),
        # Presentation layer
        ("presentation/__init__.py", None),
        ("presentation/router.py", "module/presentation/router.py.tpl"),
        ("presentation/schemas.py", "module/presentation/schemas.py.tpl"),
        ("presentation/dependencies.py", "module/presentation/dependencies.py.tpl"),
        # Application layer
        ("application/__init__.py", None),
        ("application/dto.py", "module/application/dto.py.tpl"),
        ("application/services.py", "module/application/services.py.tpl"),
        (
            "application/use_cases/__init__.py",
            "module/application/use_cases/__init__.py.tpl",
        ),
        (
            f"application/use_cases/create_{context['module_name']}_use_case.py",
            "module/application/use_cases/create_use_case.py.tpl",
        ),
        # Domain layer
        ("domain/__init__.py", None),
        ("domain/entities.py", "module/domain/entities.py.tpl"),
        ("domain/repository.py", "module/domain/repository.py.tpl"),
        ("domain/exceptions.py", "module/domain/exceptions.py.tpl"),
        ("domain/value_objects.py", "module/domain/value_objects.py.tpl"),
        # Infrastructure layer
        ("infrastructure/__init__.py", None),
        ("infrastructure/settings.py", "module/infrastructure/settings.py.tpl"),
        ("infrastructure/repositories/__init__.py", None),
        (
            "infrastructure/repositories/fake_repository.py",
            "module/infrastructure/repositories/fake_repository.py.tpl",
        ),
        ("infrastructure/gateways/__init__.py", None),
        (
            "infrastructure/gateways/httpx_gateway.py",
            "module/infrastructure/gateways/httpx_gateway.py.tpl",
        ),
        # Tests
        ("tests/__init__.py", None),
        ("tests/test_router.py", "module/tests/test_router.py.tpl"),
        ("tests/test_use_cases.py", "module/tests/test_use_cases.py.tpl"),
        ("tests/test_gateway.py", "module/tests/test_gateway.py.tpl"),
    ]

    for relative_path, template_name in structure:
        file_path = base_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        content = render_template(template_name, context) if template_name else ""
        file_path.write_text(content, encoding="utf-8")


def _register_module(module_name: str, target_dir: str | Path) -> None:
    """
    Auto-register the module's router in the project's main router.

    Creates or updates src/modules/__init__.py to include the new
    module's router so it's automatically discovered by FastAPI.
    """
    modules_init = Path(target_dir) / "__init__.py"

    if not modules_init.exists():
        modules_init.parent.mkdir(parents=True, exist_ok=True)
        modules_init.write_text(
            '"""Modules package — all routers are auto-discovered here."""\n'
            "from fastapi import APIRouter\n\n\n"
            "main_router = APIRouter()\n",
            encoding="utf-8",
        )

    content = modules_init.read_text(encoding="utf-8")
    import_line = f"from .{module_name}.presentation.router import router as {module_name}_router\n"

    if import_line not in content:
        # Add import after the docstring/module header
        lines = content.splitlines(keepends=True)
        include_line = f"main_router.include_router({module_name}_router)\n"

        # Find the right spot to insert the import
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("from ") or line.startswith("import "):
                insert_idx = i + 1
            if line.startswith("main_router"):
                insert_idx = i

        lines.insert(insert_idx, import_line)

        # Append include_router call before the last line or at end
        if include_line not in content:
            lines.append(include_line)

        modules_init.write_text("".join(lines), encoding="utf-8")
