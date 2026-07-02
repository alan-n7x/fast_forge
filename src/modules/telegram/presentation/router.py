"""
Router for telegram module.
"""

from fastapi import APIRouter

from telegram.presentation.schemas import HealthResponse

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """
    Health check endpoint for the telegram module.

    Returns:
        HealthResponse with current status.
    """
    # TODO: Add database/external service health checks
    return HealthResponse(status="ok", module="telegram")
