"""Application services for {module_name} module."""

from modules.{module_name}.application.dto import Create{entity_name}DTO, {entity_name}DTO
from modules.{module_name}.domain.entities import {entity_name}
from modules.{module_name}.domain.exceptions import {entity_name}NotFoundError
from modules.{module_name}.domain.repository import I{entity_name}Repository


class {entity_name}Service:
    """Application service orchestrating {module_name} operations.

    This service coordinates use cases and delegates to the domain layer.
    """

    def __init__(self, repository: I{entity_name}Repository) -> None:
        """Initialize the service.

        Args:
            repository: Domain repository implementation.

        """
        self._repository = repository

    async def create(self, dto: Create{entity_name}DTO) -> {entity_name}DTO:
        """Create a new {entity_name}.

        Args:
            dto: Data for creation.

        Returns:
            The created entity as a DTO.

        """
        # TODO: Add validation and business rules
        entity = {entity_name}(name=dto.name, description=dto.description)
        created = await self._repository.save(entity)
        return {entity_name}DTO(id=created.id, name=created.name, description=created.description)

    async def get_by_id(self, entity_id: str) -> {entity_name}DTO:
        """Retrieve a {entity_name} by its ID.

        Args:
            entity_id: UUID string of the entity.

        Returns:
            The matching entity as a DTO.

        Raises:
            {entity_name}NotFoundError: If not found.

        """
        entity = await self._repository.find_by_id(entity_id)
        if entity is None:
            raise {entity_name}NotFoundError(entity_id)
        return {entity_name}DTO(id=entity.id, name=entity.name, description=entity.description)
