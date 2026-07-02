"""
Infrastructure settings for telegram module.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseSettings):
    """
    Configuration settings for the telegram module.

    Reads from environment variables, .env files, or defaults.
    """

    # TODO: Add module-specific settings
    # Example: service_url: str = "http://localhost:8000"
    # Example: api_key: str = ""

    model_config = SettingsConfigDict(env_prefix="telegram_", env_file=".env")
