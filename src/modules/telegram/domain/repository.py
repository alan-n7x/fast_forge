"""
Repository interfaces for telegram module.
"""

from abc import ABC, abstractmethod

from modules.telegram.domain.entities import Telegram


class ITelegramRepository(ABC):
    """
    Repository interface for Telegram persistence.

    Follows the Dependency Inversion Principle — infrastructure
    implements this interface so the domain/application layers
    remain decoupled from storage details.
    """

    @abstractmethod
    async def save(self, entity: Telegram) -> Telegram:
        """
        Persist a Telegram.

        Args:
            entity: The entity to save.

        Returns:
            The saved entity with any updated state (e.g., generated ID).
        """
        ...

    @abstractmethod
    async def find_by_id(self, entity_id: str) -> Telegram | None:
        """
        Find a Telegram by its ID.

        Args:
            entity_id: UUID string of the entity.

        Returns:
            The entity if found, None otherwise.
        """
        ...

    @abstractmethod
    async def find_all(self) -> list[Telegram]:
        """
        Retrieve all Telegram entities.

        Returns:
            List of all entities.
        """
        ...

    @abstractmethod
    async def delete(self, entity_id: str) -> None:
        """
        Delete a Telegram by its ID.

        Args:
            entity_id: UUID string of the entity to delete.
        """
        ...
