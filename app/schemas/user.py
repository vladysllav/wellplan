from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date
from app.models.user import User as DBUser, UserTypeEnum


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserSignUp(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    date_of_birth: date


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
    date_of_birth: Optional[date] = None


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    user_type: UserTypeEnum
    date_of_birth: date

    class Config:
        orm_mode = True


class UserSignUpResponse(User):
    access_token: str
    refresh_token: str
