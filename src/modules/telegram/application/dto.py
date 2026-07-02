"""
Data transfer objects for telegram module.
"""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class CreateTelegramDTO:
    """DTO for creating a new Telegram."""

    # TODO: Add fields matching the creation input
    name: str
    description: str | None = None


@dataclass
class TelegramDTO:
    """DTO representing a Telegram in the application layer."""

    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str | None = None

    # TODO: Add additional application-level fields
