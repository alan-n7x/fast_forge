"""
HTTP gateway for {module_name} module.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, cast

import httpx


class {entity_name}Gateway:
    """
    Gateway for external HTTP APIs related to {module_name}.

    Uses httpx.AsyncClient for async HTTP communication.
    """

    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        """
        Initialize the gateway.

        Args:
            base_url: Base URL for the external API.
            api_key: Optional API key for authentication.
        """
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key

    @asynccontextmanager
    async def _client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """Create and yield an HTTP client session."""
        headers = {{}}
        if self._api_key:
            headers["Authorization"] = f"Bearer {{self._api_key}}"
        async with httpx.AsyncClient(base_url=self._base_url, headers=headers) as client:
            yield client

    async def fetch_data(self, endpoint: str) -> dict[str, Any]:
        """
        Fetch data from an external endpoint.

        Args:
            endpoint: API path (e.g., "/v1/resource").

        Returns:
            JSON response as a dict.

        Raises:
            httpx.HTTPError: On network or HTTP errors.
        """
        # TODO: Implement actual data fetching logic
        async with self._client() as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
