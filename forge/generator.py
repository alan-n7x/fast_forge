"""
Module generator — scaffolds Clean Architecture modules for FastAPI.
"""

from pathlib import Path

from forge.templates import (
    DOMAIN_ENTITIES,
    DOMAIN_EXCEPTIONS,
    DOMAIN_REPOSITORY,
    DOMAIN_VALUE_OBJECTS,
    DTO,
    DEPENDENCIES,
    FAKE_REPOSITORY,
    HTTPS_GATEWAY,
    INFRASTRUCTURE_SETTINGS,
    MODULE_INIT,
    MODULE_README,
    ROUTER,
    SCHEMAS,
    SERVICES,
    TEST_GATEWAY,
    TEST_ROUTER,
    TEST_USE_CASES,
    USE_CASE,
    USE_CASE_INIT,
)


def to_pascal_case(name: str) -> str:
    """Convert snake_case or kebab-case to PascalCase."""
    return "".join(word.capitalize() for word in name.replace("-", "_").split("_"))


def create_module(module_name: str, target_dir: str = "src/modules") -> Path:
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
    module_path = Path(target_dir) / module_name
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


def _create_structure(base_path: Path, context: dict) -> None:
    """Create the directory tree and write template files."""
    structure = [
        # Module root
        ("__init__.py", MODULE_INIT),
        ("README.md", MODULE_README),
        # Presentation layer
        ("presentation/__init__.py", ""),
        ("presentation/router.py", ROUTER),
        ("presentation/schemas.py", SCHEMAS),
        ("presentation/dependencies.py", DEPENDENCIES),
        # Application layer
        ("application/__init__.py", ""),
        ("application/dto.py", DTO),
        ("application/services.py", SERVICES),
        ("application/use_cases/__init__.py", USE_CASE_INIT),
        (
            f"application/use_cases/create_{context['module_name']}_use_case.py",
            USE_CASE,
        ),
        # Domain layer
        ("domain/__init__.py", ""),
        ("domain/entities.py", DOMAIN_ENTITIES),
        ("domain/repository.py", DOMAIN_REPOSITORY),
        ("domain/exceptions.py", DOMAIN_EXCEPTIONS),
        ("domain/value_objects.py", DOMAIN_VALUE_OBJECTS),
        # Infrastructure layer
        ("infrastructure/__init__.py", ""),
        ("infrastructure/settings.py", INFRASTRUCTURE_SETTINGS),
        ("infrastructure/repositories/__init__.py", ""),
        (
            "infrastructure/repositories/fake_repository.py",
            FAKE_REPOSITORY,
        ),
        ("infrastructure/gateways/__init__.py", ""),
        ("infrastructure/gateways/httpx_gateway.py", HTTPS_GATEWAY),
        # Tests
        ("tests/__init__.py", ""),
        ("tests/test_router.py", TEST_ROUTER),
        ("tests/test_use_cases.py", TEST_USE_CASES),
        ("tests/test_gateway.py", TEST_GATEWAY),
    ]

    for relative_path, template in structure:
        file_path = base_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if template:
            try:
                content = template.format(**context)
            except (KeyError, IndexError) as exc:
                msg = f"Error formatting template '{relative_path}': {exc}"
                raise RuntimeError(msg) from exc
        else:
            content = ""
        file_path.write_text(content, encoding="utf-8")


def _register_module(module_name: str, target_dir: str) -> None:
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
