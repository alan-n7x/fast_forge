#!/usr/bin/env python3
"""
fast_forge — CLI scaffolding generator for FastAPI Clean Architecture modules.

Usage:
    python manage.py startmodule <module_name>

Examples:
    python manage.py startmodule telegram
    python manage.py startmodule offers
    python manage.py startmodule notifications
"""

import sys
from pathlib import Path

# Ensure the project root is in sys.path so that `forge` is importable.
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from forge.cli import main

if __name__ == "__main__":
    main()
