from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps


router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(deps.get_db), user_data: schemas.UserLogin = Body(...)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    ...
