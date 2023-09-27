from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.core.config import settings
from app.core.security import hash_password, create_token
from app.crud.user import crud_user


router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(deps.get_db), user_data: schemas.UserLogin = Body(...)
) -> Any:
    """
    Endpoint to allow users to login

    :param db: DB session
    :param user_data: Body object with email and password
    :return: jwt access and refresh token
    """
    user = crud_user.authenticate(
        db, email=user_data.email, password=user_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud_user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": create_token(
            {"user_id": user.id}, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "refresh_token": create_token(
            {"user_id": user.id}, expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        ),
    }


@router.post("/sign-up", response_model=schemas.UserSignUpResponse, status_code=201)
def register_user(
    user_data: schemas.UserSignUp,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Register a new user.
    """
    existing_user = crud_user.get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )

    hashed_password = hash_password(user_data.password)
    user_data.password = hashed_password
    user = crud_user.create_user(db, user=user_data)
    response = schemas.UserSignUpResponse(
        **user.__dict__,
        access_token=create_token(
            {"user_id": user.id}, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        refresh_token=create_token(
            {"user_id": user.id}, expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        ),
    )
    return response


# @router.put("/change-password", response_model=schemas.Message)
# def change_password(
#     current_user: User = Depends(deps.get_current_user),
#     new_password: str = Body(...),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Change the user's password.
#     """
#
#     hashed_password = hash_password(new_password)
#     current_user.hashed_password = hashed_password
#     db.commit()
#     return {"msg": "Password changed successfully"}
#
#
# @router.post("/reset-password/{token}", response_model=schemas.Msg)
# def reset_password(
#     token: str,
#     new_password: str = Body(...),
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Reset the user's password using a reset token.
#     """
#
#     email = verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#
#     # Get the user by email
#     user = user.get_by_email(db, email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="User with this email does not exist",
#         )
#
#     # Update the user's password
#     hashed_password = hash_password(new_password)
#     user.hashed_password = hashed_password
#     db.commit()
#     return {"msg": "Password reset successfully"}
