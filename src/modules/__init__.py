"""Modules package — all routers are auto-discovered here."""

from fastapi import APIRouter

from .telegram.presentation.router import router as telegram_router

main_router = APIRouter()
main_router.include_router(telegram_router)
