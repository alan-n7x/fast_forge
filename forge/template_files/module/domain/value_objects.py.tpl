"""
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
