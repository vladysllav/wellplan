from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.core import security
from app.core.config import Settings

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    user_data: schemas.UserLogin = Body(...),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user.authenticate(
        db, email=user_data.username, password=user_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.token_create(
        user.id, user.email, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
