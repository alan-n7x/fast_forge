"""
Command: startmodule — generates a new Clean Architecture module.
"""

import sys

from forge.generator import create_module, normalize_module_name


def execute(args: list[str]) -> None:
    """
    Run the startmodule command.

    Usage: python manage.py startmodule <module_name>
    """
    if not args or args[0] in ("--help", "-h"):
        print("Usage: python manage.py startmodule <module_name>")
        print("")
        print("Generate a new Clean Architecture module.")
        print("")
        print("Arguments:")
        print("  <module_name>   Module name (e.g., telegram, offer_management)")
        print("")
        print("Example:")
        print("  python manage.py startmodule notifications")
        sys.exit(1)

    module_name = normalize_module_name(args[0])

    try:
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
        sys.exit(1)
