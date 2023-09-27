import argparse
from sqlalchemy.orm import Session
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

def main():
    parser = argparse.ArgumentParser(description='Create a superuser.')
    parser.add_argument('email', type=str, help='Email address for the superuser')
    parser.add_argument('password', type=str, help='Password for the superuser')

    args = parser.parse_args()
    email = args.email
    password = args.password

    create_superuser(email, hashing_password(password))

if __name__ == "__main__":
    main()