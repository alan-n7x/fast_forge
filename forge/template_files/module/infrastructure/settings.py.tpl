"""Infrastructure settings for {module_name} module."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class {entity_name}Settings(BaseSettings):
    """Configuration settings for the {module_name} module.

    Reads from environment variables, .env files, or defaults.
    """

    # TODO: Add module-specific settings
    # Example: service_url: str = "http://localhost:8000"
    # Example: api_key: str = ""

    model_config = SettingsConfigDict(env_prefix="{module_name}_", env_file=".env")
