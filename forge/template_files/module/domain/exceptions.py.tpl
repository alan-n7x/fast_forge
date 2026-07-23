"""Domain exceptions for {module_name} module."""


class {entity_name}NotFoundError(Exception):
    """Raised when a {entity_name} is not found.

    This is a domain exception, meaning it originates from
    business rules rather than infrastructure concerns.
    """

    def __init__(self, entity_id: str) -> None:
        """Initialize the exception.

        Args:
            entity_id: Identifier of the entity that was not found.

        """
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with ID '{{entity_id}}' not found")


class {entity_name}ValidationError(Exception):
    """Raised when {entity_name} data fails validation."""

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable validation failure.

        """
        super().__init__(message)
