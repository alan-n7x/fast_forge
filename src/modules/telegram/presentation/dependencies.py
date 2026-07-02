"""
Dependencies for telegram module.
"""

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telegram.infrastructure.repositories.fake_repository import (
        FakeTelegramRepository,
    )


async def get_repository() -> AsyncGenerator["FakeTelegramRepository", None]:
    """
    Provide repository instance for the telegram module.

    Yields:
        A repository instance scoped to the request.
    """
    # TODO: Replace with actual repository implementation (e.g., SQLAlchemy)
    from telegram.infrastructure.repositories.fake_repository import (
        FakeTelegramRepository,
    )

    repository = FakeTelegramRepository()
    # TODO: Add startup/cleanup logic if needed
    yield repository
