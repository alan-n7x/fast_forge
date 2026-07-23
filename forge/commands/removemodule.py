"""
Command: removemodule — removes a Clean Architecture module.
"""

import shutil
import sys
from pathlib import Path

from forge.generator import normalize_module_name, resolve_module_path


def execute(args: list[str]) -> None:
    """
    Run the removemodule command.

    Usage: python manage.py removemodule <module_name>
    """
    if not args or args[0] in ("--help", "-h"):
        print("Usage: python manage.py removemodule <module_name>")
        print("")
        print("Remove a module and its auto-registration.")
        print("")
        print("Arguments:")
        print("  <module_name>   Module name to remove")
        print("")
        print("Example:")
        print("  python manage.py removemodule telegram")
        sys.exit(1)

    module_name = normalize_module_name(args[0])
    try:
        module_path = resolve_module_path(module_name, "src/modules")
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    if not module_path.exists():
        print(f"Error: module '{module_name}' not found at {module_path}")
        sys.exit(1)

    confirm = input(f"Remove '{module_name}' and all its files? (y/N): ")
    if confirm.lower() != "y":
        print("Cancelled.")
        return

    shutil.rmtree(module_path)
    _unregister_module(module_name, module_path.parent)
    print(f"Module '{module_name}' removed.")


def _unregister_module(module_name: str, target_dir: str | Path = "src/modules") -> None:
    """Remove router import and registration from src/modules/__init__.py."""
    modules_init = Path(target_dir) / "__init__.py"
    if not modules_init.exists():
        return

    content = modules_init.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    filtered = [
        line
        for line in lines
        if f".{module_name}." not in line and f"include_router({module_name}_router)" not in line
    ]

    modules_init.write_text("".join(filtered), encoding="utf-8")
