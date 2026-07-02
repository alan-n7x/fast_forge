"""
In-memory fake repository for telegram module.
"""

from uuid import uuid4

from telegram.domain.entities import Telegram
from telegram.domain.repository import ITelegramRepository


class FakeTelegramRepository(ITelegramRepository):
    """
    In-memory implementation of ITelegramRepository.

    Uses a dict for storage. Useful for testing and development
    before a real database adapter is implemented.
    """

    def __init__(self) -> None:
        self._storage: dict[str, Telegram] = {}

    async def save(self, entity: Telegram) -> Telegram:
        """
        Persist a Telegram in memory.

        Args:
            entity: The entity to store.

        Returns:
            The stored entity.
        """
        if entity.id is None:
            entity.id = uuid4()
        self._storage[str(entity.id)] = entity
        return entity

    async def find_by_id(self, entity_id: str) -> Telegram | None:
        """
        Find a Telegram by ID.

        Args:
            entity_id: UUID string.

        Returns:
            The entity or None.
        """
        return self._storage.get(entity_id)

    async def find_all(self) -> list[Telegram]:
        """
        Return all stored entities.

        Returns:
            List of entities.
        """
        return list(self._storage.values())

    async def delete(self, entity_id: str) -> None:
        """
        Delete an entity by ID.

        Args:
            entity_id: UUID string of the entity to remove.
        """
        self._storage.pop(entity_id, None)
