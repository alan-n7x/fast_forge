"""
Pydantic schemas for telegram module.
"""

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    module: str


class TelegramBase(BaseModel):
    """Base schema with common telegram fields."""

    # TODO: Add common fields
    name: str
    description: str | None = None


class TelegramCreate(TelegramBase):
    """Schema for creating a new Telegram."""

    # TODO: Add creation-specific fields (e.g., required fields not in Base)
    pass


class TelegramUpdate(BaseModel):
    """Schema for updating an existing Telegram. All fields optional."""

    # TODO: Add updatable fields (all optional)
    name: str | None = None
    description: str | None = None


class TelegramResponse(TelegramBase):
    """Schema for Telegram API responses."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TelegramListResponse(BaseModel):
    """Schema for paginated list responses."""

    items: list[TelegramResponse]
    total: int
    page: int
    page_size: int
