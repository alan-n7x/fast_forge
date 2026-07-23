"""Domain entities for {module_name} module."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class {entity_name}:
    """Domain entity representing a {entity_name}.

    This is the core domain object with business logic and invariants.
    """

    name: str
    description: str | None = None
    id: UUID = field(default_factory=uuid4)

    # TODO: Add domain methods and business rules
    # TODO: Add value objects as needed

    def rename(self, new_name: str) -> None:
        """Change the name of the entity.

        Args:
            new_name: The new name to set.

        Raises:
            ValueError: If the new name is empty.

        """
        if not new_name:
            raise ValueError("Name cannot be empty")
        self.name = new_name
