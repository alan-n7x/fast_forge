"""
CLI entry point for fast_forge.

Usage:
    python manage.py startmodule <module_name>
    forge startmodule <module_name>
"""

import sys

from forge.commands import removemodule, startmodule

COMMANDS = {
    "startmodule": startmodule.execute,
    "removemodule": removemodule.execute,
}


def main() -> None:
    """Main CLI dispatcher."""
    args = sys.argv[1:]

    if not args:
        _print_help()
        return

    if args[0] in ("--help", "-h", "help"):
        _print_help()
        return

    command = args[0]

    if command not in COMMANDS:
        print(f"Unknown command: '{command}'")
        print(f"Available commands: {', '.join(COMMANDS)}")
        sys.exit(1)

    COMMANDS[command](args[1:])


def _print_help() -> None:
    """Display available commands."""
    print("fast_forge — Clean Architecture module generator for FastAPI")
    print("")
    print("Usage:")
    print("  python manage.py <command> [options]")
    print("")
    print("Commands:")
    print("  startmodule  <name> [--dry-run]          Generate a module")
    print("  removemodule <name> [--dry-run|--force]  Remove a module")
    print("")


if __name__ == "__main__":
    main()
