"""
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
