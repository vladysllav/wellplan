import os
from datetime import datetime, timedelta

import jwt

from fastapi.security import APIKeyHeader
from passlib.context import CryptContext

from app.core.config import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
apikey_scheme = APIKeyHeader(name="Authorization")


def create_token(data: dict, expire_minutes: int | None = None):
    to_encode = data.copy()
    if expire_minutes:
        expire = datetime.utcnow() + timedelta(expire_minutes)
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.AUTHENTICATION__ALGORITHM)
    return encoded_jwt


def create_reset_token(user_id: int, expire_minutes: int):
    to_encode = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expire_minutes),
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.AUTHENTICATION__ALGORITHM)


def token_decode(token: str):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.AUTHENTICATION__ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:

        return None
    except jwt.DecodeError:

        return None


def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.AUTHENTICATION__ALGORITHM])
        user_id = int(payload.get("user_id"))
        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None


def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str):
    return password_context.hash(plain_password)


def verify_refresh_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.AUTHENTICATION__ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:

        return None
    except jwt.DecodeError:

        return False


def create_refresh_token(data: dict, expire_minutes: int | None = None):
    to_encode = data.copy()
    if expire_minutes:
        expire = datetime.utcnow() + timedelta(expire_minutes)
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.AUTHENTICATION__ALGORITHM)
    return encoded_jwt
