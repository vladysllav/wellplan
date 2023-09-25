from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app.api.auth import routes as auth_routes
from app.api.deps import get_db
from app.crud.base import CRUDBase
from app.api.users import routes as user_routes


from app.models import Branch, Doctor
from app.schemas.doctor import (BaseBranch, BaseDoctor, BranchUpdate,
                                CreateBranch, CreateDoctor, DoctorUpdate)
from fastapi import APIRouter
from app.api.auth import routes

from app.api.auth import routes as auth_routes
from app.api.doctors import routes as doctor_router
from app.api.doctors import routes as branch_router


api_router = APIRouter()

api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
api_router.include_router(doctor_router.doctors_router, prefix="/doctors", tags=["doctors"])
api_router.include_router(branch_router.branches_router, prefix="/branches", tags=["branches"])


@api_router.post("/alive")
def alive() -> Any:
    """
    Default alive endpoint
    """
    return {"status": "ok"}
