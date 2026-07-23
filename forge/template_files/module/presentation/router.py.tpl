"""
Router for {module_name} module.
"""

from fastapi import APIRouter

from modules.{module_name}.presentation.schemas import HealthResponse

router = APIRouter(prefix="/{module_name}", tags=["{module_name}"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """
    Health check endpoint for the {module_name} module.

    Returns:
        HealthResponse with current status.
    """
    # TODO: Add database/external service health checks
    return HealthResponse(status="ok", module="{module_name}")
