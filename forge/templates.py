"""Template strings for generated module files."""

MODULE_INIT = '''"""
{module_name} module.
"""
'''

MODULE_README = """# {ModuleName} Module

## Clean Architecture Structure

- **presentation/**: API routers, schemas, and dependencies
- **application/**: Use cases, services, and DTOs
- **domain/**: Entities, repository interfaces, exceptions, and value objects
- **infrastructure/**: Repository implementations, external gateways, and settings
- **tests/**: Unit and integration tests

## TODO

- [ ] Implement domain entities
- [ ] Implement repository interface
- [ ] Implement use cases
- [ ] Implement API endpoints
- [ ] Implement external gateways
- [ ] Write tests
"""

ROUTER = '''"""
Router for {module_name} module.
"""

from fastapi import APIRouter

from modules.{module_name}.presentation.schemas import HealthResponse

router = APIRouter(prefix="/{module_name}", tags=["{module_name}"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """
    Health check endpoint for the {module_name} module.

    Returns:
        HealthResponse with current status.
    """
    # TODO: Add database/external service health checks
    return HealthResponse(status="ok", module="{module_name}")
'''

SCHEMAS = '''"""
Pydantic schemas for {module_name} module.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    module: str


class {entity_name}Base(BaseModel):
    """Base schema with common {module_name} fields."""

    # TODO: Add common fields
    name: str
    description: str | None = None


class {entity_name}Create({entity_name}Base):
    """Schema for creating a new {entity_name}."""

    # TODO: Add creation-specific fields (e.g., required fields not in Base)
    pass


class {entity_name}Update(BaseModel):
    """Schema for updating an existing {entity_name}. All fields optional."""

    # TODO: Add updatable fields (all optional)
    name: str | None = None
    description: str | None = None


class {entity_name}Response({entity_name}Base):
    """Schema for {entity_name} API responses."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class {entity_name}ListResponse(BaseModel):
    """Schema for paginated list responses."""

    items: list[{entity_name}Response]
    total: int
    page: int
    page_size: int
'''

DEPENDENCIES = '''"""
Dependencies for {module_name} module.
"""

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.{module_name}.infrastructure.repositories.fake_repository import (
        Fake{entity_name}Repository,
    )


async def get_repository() -> AsyncGenerator["Fake{entity_name}Repository", None]:
    """
    Provide repository instance for the {module_name} module.

    Yields:
        A repository instance scoped to the request.
    """
    # TODO: Replace with actual repository implementation (e.g., SQLAlchemy)
    from modules.{module_name}.infrastructure.repositories.fake_repository import (
        Fake{entity_name}Repository,
    )

    repository = Fake{entity_name}Repository()
    # TODO: Add startup/cleanup logic if needed
    yield repository
'''

DTO = '''"""
Data transfer objects for {module_name} module.
"""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Create{entity_name}DTO:
    """DTO for creating a new {entity_name}."""

    # TODO: Add fields matching the creation input
    name: str
    description: str | None = None


@dataclass
class {entity_name}DTO:
    """DTO representing a {entity_name} in the application layer."""

    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str | None = None

    # TODO: Add additional application-level fields
'''

SERVICES = '''"""
Application services for {module_name} module.
"""

from modules.{module_name}.application.dto import Create{entity_name}DTO, {entity_name}DTO
from modules.{module_name}.domain.entities import {entity_name}
from modules.{module_name}.domain.exceptions import {entity_name}NotFoundError
from modules.{module_name}.domain.repository import I{entity_name}Repository


class {entity_name}Service:
    """
    Application service orchestrating {module_name} operations.

    This service coordinates use cases and delegates to the domain layer.
    """

    def __init__(self, repository: I{entity_name}Repository) -> None:
        """
        Initialize the service.

        Args:
            repository: Domain repository implementation.
        """
        self._repository = repository

    async def create(self, dto: Create{entity_name}DTO) -> {entity_name}DTO:
        """
        Create a new {entity_name}.

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
        """
        Retrieve a {entity_name} by its ID.

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
'''

DOMAIN_ENTITIES = '''"""
Domain entities for {module_name} module.
"""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class {entity_name}:
    """
    Domain entity representing a {entity_name}.

    This is the core domain object with business logic and invariants.
    """

    name: str
    description: str | None = None
    id: UUID = field(default_factory=uuid4)

    # TODO: Add domain methods and business rules
    # TODO: Add value objects as needed

    def rename(self, new_name: str) -> None:
        """
        Change the name of the entity.

        Args:
            new_name: The new name to set.

        Raises:
            ValueError: If the new name is empty.
        """
        if not new_name:
            raise ValueError("Name cannot be empty")
        self.name = new_name
'''

DOMAIN_REPOSITORY = '''"""
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
'''

DOMAIN_EXCEPTIONS = '''"""
Domain exceptions for {module_name} module.
"""


class {entity_name}NotFoundError(Exception):
    """
    Raised when a {entity_name} is not found.

    This is a domain exception, meaning it originates from
    business rules rather than infrastructure concerns.
    """

    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with ID '{{entity_id}}' not found")


class {entity_name}ValidationError(Exception):
    """
    Raised when {entity_name} data fails validation.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
'''

DOMAIN_VALUE_OBJECTS = '''"""
Value objects for {module_name} module.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class {entity_name}Status:
    """
    Immutable value object representing a {entity_name} status.

    Value objects are defined by their attributes and have no identity.
    They should be immutable.
    """

    value: str

    # TODO: Add valid status constants
    # ACTIVE = "active"
    # INACTIVE = "inactive"

    def __post_init__(self) -> None:
        """Validate the status value."""
        # TODO: Implement validation logic
        if not self.value:
            raise ValueError("Status value cannot be empty")
'''

INFRASTRUCTURE_SETTINGS = '''"""
Infrastructure settings for {module_name} module.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class {entity_name}Settings(BaseSettings):
    """
    Configuration settings for the {module_name} module.

    Reads from environment variables, .env files, or defaults.
    """

    # TODO: Add module-specific settings
    # Example: service_url: str = "http://localhost:8000"
    # Example: api_key: str = ""

    model_config = SettingsConfigDict(env_prefix="{module_name}_", env_file=".env")
'''

FAKE_REPOSITORY = '''"""
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
'''

USE_CASE = '''"""
Use case: {module_name} {use_case_name}.
"""

from modules.{module_name}.application.dto import Create{entity_name}DTO, {entity_name}DTO
from modules.{module_name}.domain.repository import I{entity_name}Repository


class Create{entity_name}UseCase:
    """
    Create a new {entity_name}.

    This use case encapsulates the business logic for creating
    a {entity_name} entity, including validation and side effects.
    """

    def __init__(self, repository: I{entity_name}Repository) -> None:
        """
        Initialize the use case.

        Args:
            repository: Domain repository implementation.
        """
        self._repository = repository

    async def execute(self, dto: Create{entity_name}DTO) -> {entity_name}DTO:
        """
        Execute the use case.

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
'''

USE_CASE_INIT = '"""Use cases for {module_name} module."""\n'

TEST_ROUTER = '''"""
Tests for the {module_name} router.
"""

from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from modules.{module_name}.presentation.router import router


@pytest.fixture
def app() -> FastAPI:
    """Create a test app with the {module_name} router."""
    application = FastAPI()
    application.include_router(router)
    return application


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient) -> None:
    """Test the health check endpoint returns OK."""
    response = await client.get("/{module_name}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["module"] == "{module_name}"
'''

TEST_USE_CASES = '''"""
Tests for the {module_name} use cases.
"""

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
'''

TEST_GATEWAY = '''"""
Tests for the {module_name} gateway.
"""

# TODO: Implement gateway tests
# @pytest.mark.asyncio
# async def test_gateway_placeholder() -> None:
#     """Placeholder test for gateway."""
#     assert True
'''

HTTPS_GATEWAY = '''"""
HTTP gateway for {module_name} module.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, cast

import httpx


class {entity_name}Gateway:
    """
    Gateway for external HTTP APIs related to {module_name}.

    Uses httpx.AsyncClient for async HTTP communication.
    """

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        """
        Initialize the gateway.

        Args:
            base_url: Base URL for the external API.
            api_key: Optional API key for authentication.
        """
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    @asynccontextmanager
    async def _client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """Create and yield an HTTP client session."""
        headers = {{}}
        if self._api_key:
            headers["Authorization"] = f"Bearer {{self._api_key}}"
        async with httpx.AsyncClient(base_url=self._base_url, headers=headers) as client:
            yield client

    async def fetch_data(self, endpoint: str) -> dict[str, Any]:
        """
        Fetch data from an external endpoint.

        Args:
            endpoint: API path (e.g., "/v1/resource").

        Returns:
            JSON response as a dict.

        Raises:
            httpx.HTTPError: On network or HTTP errors.
        """
        # TODO: Implement actual data fetching logic
        async with self._client() as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
'''
