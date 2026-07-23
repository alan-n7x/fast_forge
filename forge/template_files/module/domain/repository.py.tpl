"""
Repository interfaces for {module_name} module.
"""

from abc import ABC, abstractmethod

from modules.{module_name}.domain.entities import {entity_name}


class I{entity_name}Repository(ABC):
    """
    Repository interface for {entity_name} persistence.

    Follows the Dependency Inversion Principle — infrastructure
    implements this interface so the domain/application layers
    remain decoupled from storage details.
    """

    @abstractmethod
    async def save(self, entity: {entity_name}) -> {entity_name}:
        """
        Persist a {entity_name}.

        Args:
            entity: The entity to save.

        Returns:
            The saved entity with any updated state (e.g., generated ID).
        """
        ...

    @abstractmethod
    async def find_by_id(self, entity_id: str) -> {entity_name} | None:
        """
        Find a {entity_name} by its ID.

        Args:
            entity_id: UUID string of the entity.

        Returns:
            The entity if found, None otherwise.
        """
        ...

    @abstractmethod
    async def find_all(self) -> list[{entity_name}]:
        """
        Retrieve all {entity_name} entities.

        Returns:
            List of all entities.
        """
        ...

    @abstractmethod
    async def delete(self, entity_id: str) -> None:
        """
        Delete a {entity_name} by its ID.

        Args:
            entity_id: UUID string of the entity to delete.
        """
        ...
