from typing import Optional

from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    username: EmailStr
    password: str
