import argparse
from app.crud.user import CRUDUser
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.db.session import SessionLocal

def create_superuser(email: str, password: str):
    db = SessionLocal()
    crud_user = CRUDUser()
    user = crud_user.get_user_by_email(db, email=email)
    
    if not user:
        user_in = UserCreate(
            email=email,
            password=hash_password(password),
            is_superuser=True,
        )
        CRUDUser.create(db, obj_in=user_in)
        print("Superuser created successfully.")
    else:
        print("Superuser with this email already exists.")

def main():
    parser = argparse.ArgumentParser(description='Create a superuser.')
    parser.add_argument('first_name', type=str, help='First name of tge superuser')
    parser.add_argument('last_name', type=str, help='Last name of the superuser')
    parser.add_argument('email', type=str, help='Email address for the superuser')
    parser.add_argument('password', type=str, help='Password for the superuser')

    args = parser.parse_args()
    first_name = args.first_name
    last_name = args.last_name
    email = args.email
    password = args.password

    create_superuser(first_name, last_name, email, password)

if __name__ == "__main__":
    main()
