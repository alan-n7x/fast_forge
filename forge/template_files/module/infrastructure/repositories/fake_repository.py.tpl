"""
In-memory fake repository for {module_name} module.
"""

from uuid import uuid4

from modules.{module_name}.domain.entities import {entity_name}
from modules.{module_name}.domain.repository import I{entity_name}Repository


class Fake{entity_name}Repository(I{entity_name}Repository):
    """
    In-memory implementation of I{entity_name}Repository.

    Uses a dict for storage. Useful for testing and development
    before a real database adapter is implemented.
    """

    def __init__(self) -> None:
        self._storage: dict[str, {entity_name}] = {{}}

    async def save(self, entity: {entity_name}) -> {entity_name}:
        """
        Persist a {entity_name} in memory.

        Args:
            entity: The entity to store.

        Returns:
            The stored entity.
        """
        if entity.id is None:
            entity.id = uuid4()
        self._storage[str(entity.id)] = entity
        return entity

    async def find_by_id(self, entity_id: str) -> {entity_name} | None:
        """
        Find a {entity_name} by ID.

        Args:
            entity_id: UUID string.

        Returns:
            The entity or None.
        """
        return self._storage.get(entity_id)

    async def find_all(self) -> list[{entity_name}]:
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
