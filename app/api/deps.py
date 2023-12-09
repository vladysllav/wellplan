from typing import Generator

from app.db.session import SessionLocal

from datetime import datetime


from fastapi import Depends, HTTPException
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import token_decode, apikey_scheme

from app.models.user import User, UserTypeEnum
from app.crud.user import crud_user


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(apikey_scheme), db: Session = Depends(get_db)):
    try:
        token_data = token_decode(token)

        if token_data.get('exp') and datetime.fromtimestamp(token_data['exp']) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = crud_user.get_user(db, token_data['user_id'])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


def check_active_user(user: User = Depends(get_current_user)):
    if user.is_active:
        return user

    raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not active account",
    )


def check_admin(user: User = Depends(check_active_user)):
    if user.user_type == UserTypeEnum.admin:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Insufficient access rights",
        headers={"WWW-Authenticate": "Bearer"},
    )
