"""Use case: {module_name} create_{module_name}."""

from modules.{module_name}.application.dto import Create{entity_name}DTO, {entity_name}DTO
from modules.{module_name}.domain.repository import I{entity_name}Repository


class Create{entity_name}UseCase:
    """Create a new {entity_name}.

    This use case encapsulates the business logic for creating
    a {entity_name} entity, including validation and side effects.
    """

    def __init__(self, repository: I{entity_name}Repository) -> None:
        """Initialize the use case.

        Args:
            repository: Domain repository implementation.

        """
        self._repository = repository

    async def execute(self, dto: Create{entity_name}DTO) -> {entity_name}DTO:
        """Execute the use case.

        Args:
            dto: Input data for creation.

        Returns:
            The created entity DTO.

        """
        # TODO: Add business rules, validation, and side effects
        from modules.{module_name}.domain.entities import {entity_name}

        entity = {entity_name}(name=dto.name, description=dto.description)
        saved = await self._repository.save(entity)
        return {entity_name}DTO(
            id=saved.id,
            name=saved.name,
            description=saved.description,
        )
