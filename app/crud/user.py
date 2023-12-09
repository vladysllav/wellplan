from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session


from app.core.security import verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate





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


crud_user = CRUDUser(User)
