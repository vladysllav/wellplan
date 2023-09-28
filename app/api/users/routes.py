from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api.deps import get_db
from app.crud.user import crud_user

router = APIRouter()


# @router.get("/profile", response_model=schemas.User)
# def read_user_profile(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
#     user_info_from_db = crud_user.get_user_by_id(db, current_user.id)
#     if user_info_from_db is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user_info_from_db
#


@router.patch("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, user_in: schemas.UserUpdate, db: Session = Depends(get_db)
):
    user = crud_user.user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = crud_user.user.update_user(db, user, user_in)
    return updated_user
