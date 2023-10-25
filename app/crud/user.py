from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException
from jose import jwt
from pydantic import EmailStr, ValidationError
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import verify_password, token_decode, apikey_scheme
from app.crud.base import CRUDBase
from app.models.user import User, UserTypeEnum
from app.schemas.user import UserCreate, UserUpdate


from app.api import deps


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_user_by_email(self, db: Session, email: EmailStr) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(self.model).filter(self.model.id == user_id).first()

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def get_current_user(self, token: str = Depends(apikey_scheme), db: Session = Depends(deps.get_db)):
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
        user = self.get_user(db, token_data['user_id'])

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        return user


crud_user = CRUDUser(User)
