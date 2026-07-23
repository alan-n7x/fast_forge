"""Tests for the telegram use cases."""

import pytest

from modules.telegram.application.dto import CreateTelegramDTO
from modules.telegram.application.use_cases.create_telegram_use_case import (
    CreateTelegramUseCase,
)
from modules.telegram.infrastructure.repositories.fake_repository import (
    FakeTelegramRepository,
)


@pytest.fixture
def repository() -> FakeTelegramRepository:
    """Provide a fresh fake repository for each test."""
    return FakeTelegramRepository()


@pytest.mark.asyncio
async def test_create_entity(repository: FakeTelegramRepository) -> None:
    """Test creating a Telegram via the use case."""
    use_case = CreateTelegramUseCase(repository)
    dto = CreateTelegramDTO(name="Test Telegram", description="A test description")
    result = await use_case.execute(dto)
    assert result.name == "Test Telegram"
    assert result.description == "A test description"
    assert result.id is not None
