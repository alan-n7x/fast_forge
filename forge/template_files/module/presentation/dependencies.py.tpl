"""
Dependencies for {module_name} module.
"""

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.{module_name}.infrastructure.repositories.fake_repository import (
        Fake{entity_name}Repository,
    )


async def get_repository() -> AsyncGenerator["Fake{entity_name}Repository", None]:
    """
    Provide repository instance for the {module_name} module.

    Yields:
        A repository instance scoped to the request.
    """
    # TODO: Replace with actual repository implementation (e.g., SQLAlchemy)
    from modules.{module_name}.infrastructure.repositories.fake_repository import (
        Fake{entity_name}Repository,
    )

    repository = Fake{entity_name}Repository()
    # TODO: Add startup/cleanup logic if needed
    yield repository
