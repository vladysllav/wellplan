from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser:
    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: UserCreate):
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_user(self, db: Session, user_id: int, user: UserUpdate):
        db_user = db.query(User).filter(User.id == user_id).first()
        for field, value in user.dict().items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        db.delete(db_user)
        db.commit()
        return db_user


crud_user = CRUDUser()
