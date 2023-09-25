from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date
from app.models.user import User as DBUser


class UserLogin(BaseModel):
    username: EmailStr
    password: str


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    user_type: str
    date_of_birth: date


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    user_type: Optional[str] = None
    date_of_birth: Optional[date] = None


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    user_type: str
    date_of_birth: date

    class Config:
        orm_mode = True
