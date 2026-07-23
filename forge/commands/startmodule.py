"""
Command: startmodule — generates a new Clean Architecture module.
"""

import argparse

from forge.generator import create_module, normalize_module_name, plan_module


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="forge startmodule",
        description="Generate a new Clean Architecture module.",
    )
    parser.add_argument("module_name", help="Module name, such as notifications")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and show the target without creating files",
    )
    return parser


def execute(args: list[str]) -> None:
    """
    Run the startmodule command.

    Usage: python manage.py startmodule <module_name> [--dry-run]
    """
    parser = _parser()
    if not args:
        parser.print_help()
        raise SystemExit(1)

    parsed = parser.parse_args(args)
    module_name = normalize_module_name(parsed.module_name)

    try:
        if parsed.dry_run:
            path = plan_module(module_name)
            print(f"Dry run: module '{module_name}' would be created at {path}")
            print(f"Dry run: router would be registered in {path.parent / '__init__.py'}")
            return

        path = create_module(module_name)
        print(f"Module '{module_name}' created at {path}")
        print("")
        print("Next steps:")
        print(f"  1. Implement domain entities in {path / 'domain/entities.py'}")
        print(f"  2. Implement repository interface in {path / 'domain/repository.py'}")
        print(f"  3. Implement use cases in {path / 'application/use_cases/'}")
        print(f"  4. Implement API endpoints in {path / 'presentation/router.py'}")
        print(f"  5. Write tests in {path / 'tests/'}")
    except (FileExistsError, ValueError) as exc:
        print(f"Error: {exc}")
        raise SystemExit(1) from exc
