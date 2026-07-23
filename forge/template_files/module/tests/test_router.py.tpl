"""Tests for the {module_name} router."""

from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from modules.{module_name}.presentation.router import router


@pytest.fixture
def app() -> FastAPI:
    """Create a test app with the {module_name} router."""
    application = FastAPI()
    application.include_router(router)
    return application


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient) -> None:
    """Test the health check endpoint returns OK."""
    response = await client.get("/{module_name}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["module"] == "{module_name}"
