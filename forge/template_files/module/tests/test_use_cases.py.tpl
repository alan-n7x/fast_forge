"""Tests for the {module_name} use cases."""

import pytest

from modules.{module_name}.application.dto import Create{entity_name}DTO
from modules.{module_name}.application.use_cases.create_{module_name}_use_case import (
    Create{entity_name}UseCase,
)
from modules.{module_name}.infrastructure.repositories.fake_repository import (
    Fake{entity_name}Repository,
)


@pytest.fixture
def repository() -> Fake{entity_name}Repository:
    """Provide a fresh fake repository for each test."""
    return Fake{entity_name}Repository()


@pytest.mark.asyncio
async def test_create_entity(repository: Fake{entity_name}Repository) -> None:
    """Test creating a {entity_name} via the use case."""
    use_case = Create{entity_name}UseCase(repository)
    dto = Create{entity_name}DTO(name="Test {entity_name}", description="A test description")
    result = await use_case.execute(dto)
    assert result.name == "Test {entity_name}"
    assert result.description == "A test description"
    assert result.id is not None
