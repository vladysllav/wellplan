from typing import Any

from fastapi import APIRouter
from app.api.auth import routes as auth_routes

api_router = APIRouter()

api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])


@api_router.post("/alive")
def alive() -> Any:
    """
    Default alive endpoint
    """
    return {"status": "ok"}
