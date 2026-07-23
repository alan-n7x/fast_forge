"""Command: removemodule — removes a Clean Architecture module."""

import argparse
import shutil
from pathlib import Path

from forge.generator import normalize_module_name, resolve_module_path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="forge removemodule",
        description="Remove a module and its router registration.",
    )
    parser.add_argument("module_name", help="Name of the module to remove")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without changing files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Remove without an interactive confirmation",
    )
    return parser


def execute(args: list[str]) -> None:
    """Run the removemodule command.

    Usage: python manage.py removemodule <module_name> [--dry-run] [--force]
    """
    parser = _parser()
    if not args:
        parser.print_help()
        raise SystemExit(1)

    parsed = parser.parse_args(args)
    module_name = normalize_module_name(parsed.module_name)
    try:
        module_path = resolve_module_path(module_name, "src/modules")
    except ValueError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1) from exc

    if not module_path.exists():
        print(f"Error: module '{module_name}' not found at {module_path}")
        raise SystemExit(1)

    if parsed.dry_run:
        registry_path = module_path.parent / "__init__.py"
        print(f"Dry run: module directory would be removed: {module_path}")
        print(f"Dry run: router registration would be removed from {registry_path}")
        return

    if not parsed.force:
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

    modules_init.write_text("".join(filtered), encoding="utf-8", newline="\n")
