import os
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def token_create(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def token_decode(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Handle token expiration
        return None
    except jwt.DecodeError:
        # Handle token decoding error
        return None


def verifying_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


def hashing_password(plain_password: str):
    return password_context.hash(plain_password)

