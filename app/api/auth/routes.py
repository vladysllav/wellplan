from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.core.security import hashing_password


router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), user_data: schemas.UserLogin = Body(...)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    ...

@router.post("/register", response_model=schemas.User)
def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Register a new user.
    """
    existing_user = user.get_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )

    # Create the user
    user = user.create(db, obj_in=user_data)
    return user


@router.put("/change-password", response_model=schemas.Message)
def change_password(
    current_user: User = Depends(deps.get_current_user),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Change the user's password.
    """

    hashed_password = hashing_password(new_password)
    current_user.hashed_password = hashed_password
    db.commit()
    return {"msg": "Password changed successfully"}


@router.post("/reset-password/{token}", response_model=schemas.Msg)
def reset_password(
    token: str,
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset the user's password using a reset token.
    """
    
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")

    # Get the user by email
    user = user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exist",
        )

    # Update the user's password
    hashed_password = hashing_password(new_password)
    user.hashed_password = hashed_password
    db.commit()
    return {"msg": "Password reset successfully"}
