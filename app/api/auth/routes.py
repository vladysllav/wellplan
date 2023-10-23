import os
from typing import Any, Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.core.config import settings
from app.core.security import create_token, hash_password, create_reset_token, verify_reset_token, apikey_scheme, \
    create_refresh_token, verify_refresh_token
from app.crud.user import crud_user
from app.models import User
from app.schemas.email import ResponseMessage
from app.email import send_reset_password_email

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(db: Session = Depends(deps.get_db), user_data: schemas.UserLogin = Body(...)) -> Any:
    """
    Endpoint to allow users to login

    :param db: DB session
    :param user_data: Body object with email and password
    :return: jwt access and refresh token
    """
    user = crud_user.authenticate(db, email=user_data.email, password=user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": create_token({"user_id": user.id}, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "refresh_token": create_token({"user_id": user.id}, expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    }


@router.post("/sign-up", response_model=schemas.UserSignUpResponse, status_code=201)
def register_user(user_data: schemas.UserSignUp, db: Session = Depends(deps.get_db)) -> Any:
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
    user = crud_user.create(db, obj_in=user_data)
    response = schemas.UserSignUpResponse(
        **user.__dict__,
        access_token=create_token({"user_id": user.id}, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh_token=create_token({"user_id": user.id}, expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    return response


@router.post("/forgot-password", response_model=ResponseMessage, status_code=201)
def forgot_password(user_email: str = Body(...), db: Session = Depends(deps.get_db)):
    user = crud_user.get_user_by_email(db, email=user_email)
    if not user:
        return ResponseMessage(message=f"An email has been sent to {user_email} with a link to reset your password.")

    reset_token = create_reset_token(user.id, int(os.getenv("FORGOT_PASSWORD_TOKEN_EXPIRE_MINUTES")))
    base_url = os.getenv("BASE_URL")  # test url
    reset_url = f"{base_url}/reset-password/{reset_token}"
    send_reset_password_email(user_email, reset_url)

    return ResponseMessage(message=f"An email has been sent to {user_email} with a link to reset your password.")


@router.post("/authentication", response_model=schemas.UserAuth, status_code=200)
def auth(access_token: Annotated[str, Depends(apikey_scheme)], db: Session = Depends(deps.get_db)):
    user = crud_user.get_current_user(db, access_token)

    if not user:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    user_auth = schemas.UserAuth(**user.__dict__)
    return user_auth


@router.post("/refresh", response_model=schemas.RefreshToken)
async def refresh_token(token: str = Body(...), db: Session = Depends(deps.get_db), user: User = Depends(auth)):
    decoded_token = verify_refresh_token(token)

    if decoded_token is False:
        raise HTTPException(status_code=400, detail="Invalid token")

    if decoded_token is None:
        new_access_token = create_token(data=decoded_token)
        return {
            "access_token": new_access_token,
            "refresh_token": None
        }

    new_refresh_token = create_refresh_token(data=decoded_token)
    return {
        "refresh_token": new_refresh_token,
        "access_token": None
    }


@router.post("/reset-password", response_model=ResponseMessage, status_code=200)
def reset_password(
    reset_token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
    user: User = Depends(auth)
):
    user_id = verify_reset_token(reset_token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid reset token")

    user = crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hash_password(new_password)
    user.password = hashed_password
    db.commit()
    return ResponseMessage(message="Password reset successfully")


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
