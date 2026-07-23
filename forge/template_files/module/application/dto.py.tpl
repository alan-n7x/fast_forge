"""Data transfer objects for {module_name} module."""

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
