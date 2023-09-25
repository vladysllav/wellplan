import sys
from sqlalchemy.orm import Session
from app.crud.user import UserCreate
from app.models.user import User
from app.schemas.user import *
from app.core.security import hashing_password
from app.db.session import SessionLocal

def create_superuser(email: str, password: str):
    db = SessionLocal()
    user = user.get_by_email(db, email=email)
    if not user:
        user_in = UserCreate(
            email=email,
            password=password,
            full_name="Superuser",
            is_superuser=True,
        )
        user = user.create(db, obj_in=user_in)
        print("Superuser created successfully.")
    else:
        print("Superuser with this email already exists.")

if len(sys.argv) != 3:
    print("Usage: python create_superuser.py <email> <password>")
    sys.exit(1)

email = sys.argv[1]
password = sys.argv[2]

create_superuser(email, hashing_password(password))
