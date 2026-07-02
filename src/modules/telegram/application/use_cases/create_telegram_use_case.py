"""
Use case: telegram create_telegram.
"""

from telegram.application.dto import CreateTelegramDTO, TelegramDTO
from telegram.domain.repository import ITelegramRepository


class CreateTelegramUseCase:
    """
    Create a new Telegram.

    This use case encapsulates the business logic for creating
    a Telegram entity, including validation and side effects.
    """

    def __init__(self, repository: ITelegramRepository) -> None:
        """
        Initialize the use case.

        Args:
            repository: Domain repository implementation.
        """
        self._repository = repository

    async def execute(self, dto: CreateTelegramDTO) -> TelegramDTO:
        """
        Execute the use case.

        Args:
            dto: Input data for creation.

        Returns:
            The created entity DTO.
        """
        # TODO: Add business rules, validation, and side effects
        from telegram.domain.entities import Telegram

        entity = Telegram(name=dto.name, description=dto.description)
        saved = await self._repository.save(entity)
        return TelegramDTO(
            id=saved.id,
            name=saved.name,
            description=saved.description,
        )
