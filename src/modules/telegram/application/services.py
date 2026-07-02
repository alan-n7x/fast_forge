"""
Application services for telegram module.
"""

from telegram.application.dto import CreateTelegramDTO, TelegramDTO
from telegram.domain.entities import Telegram
from telegram.domain.exceptions import TelegramNotFoundError
from telegram.domain.repository import ITelegramRepository


class TelegramService:
    """
    Application service orchestrating telegram operations.

    This service coordinates use cases and delegates to the domain layer.
    """

    def __init__(self, repository: ITelegramRepository) -> None:
        """
        Initialize the service.

        Args:
            repository: Domain repository implementation.
        """
        self._repository = repository

    async def create(self, dto: CreateTelegramDTO) -> TelegramDTO:
        """
        Create a new Telegram.

        Args:
            dto: Data for creation.

        Returns:
            The created entity as a DTO.
        """
        # TODO: Add validation and business rules
        entity = Telegram(name=dto.name, description=dto.description)
        created = await self._repository.save(entity)
        return TelegramDTO(id=created.id, name=created.name, description=created.description)

    async def get_by_id(self, entity_id: str) -> TelegramDTO:
        """
        Retrieve a Telegram by its ID.

        Args:
            entity_id: UUID string of the entity.

        Returns:
            The matching entity as a DTO.

        Raises:
            TelegramNotFoundError: If not found.
        """
        entity = await self._repository.find_by_id(entity_id)
        if entity is None:
            raise TelegramNotFoundError(entity_id)
        return TelegramDTO(id=entity.id, name=entity.name, description=entity.description)
