"""Domain exceptions for telegram module."""


class TelegramNotFoundError(Exception):
    """Raised when a Telegram is not found.

    This is a domain exception, meaning it originates from
    business rules rather than infrastructure concerns.
    """

    def __init__(self, entity_id: str) -> None:
        """Initialize the exception.

        Args:
            entity_id: Identifier of the entity that was not found.

        """
        self.entity_id = entity_id
        super().__init__(f"Telegram with ID '{entity_id}' not found")


class TelegramValidationError(Exception):
    """Raised when Telegram data fails validation."""

    def __init__(self, message: str) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable validation failure.

        """
        super().__init__(message)
