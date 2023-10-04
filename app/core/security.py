import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(data: dict, expire_minutes: int | None = None):
    to_encode = data.copy()
    if expire_minutes:
        expire = datetime.utcnow() + timedelta(expire_minutes)
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.AUTHENTICATION__ALGORITHM
    )
    return encoded_jwt


def token_decode(token: str):
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.AUTHENTICATION__ALGORITHM]
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Handle token expiration
        return None
    except jwt.DecodeError:
        # Handle token decoding error
        return None


def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str):
    return password_context.hash(plain_password)
