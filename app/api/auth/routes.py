from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.crud.base import CRUDBase
from app.models import Doctor, Branch
from app.schemas.doctor import CreateDoctor, DoctorUpdate, CreateBranch, BranchUpdate, BaseDoctor, BaseBranch
from app.api.deps import get_db

router = APIRouter()

doctors_router = APIRouter()
branches_router = APIRouter()

crud_doctor = CRUDBase(Doctor)
crud_branch = CRUDBase(Branch)


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(deps.get_db), user_data: schemas.UserLogin = Body(...)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    ...


@doctors_router.post("/doctors/", response_model=CreateDoctor, status_code=status.HTTP_201_CREATED)
def create_doctor(obj_in: CreateDoctor, db: Session = Depends(get_db)):
    doctor = crud_doctor.create(db, obj_in=obj_in)

    return doctor


@doctors_router.get("/doctors/", response_model=list[BaseDoctor], status_code=status.HTTP_200_OK)
def get_doctor_list(db: Session = Depends(get_db)):
    doctors = crud_doctor.get_multi(db)

    return doctors


@doctors_router.get("/doctors/{doctor_id}", response_model=BaseDoctor, status_code=status.HTTP_200_OK)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud_doctor.get(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor


@doctors_router.put("/doctors/{doctor_id}", response_model=DoctorUpdate, status_code=status.HTTP_200_OK)
def update_doctor(doctor_id: int, obj_in: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = crud_doctor.get(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor = crud_doctor.update(db, db_obj=doctor, obj_in=obj_in)

    return doctor


@doctors_router.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_obj = crud_doctor.get(db, doctor_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db_obj = crud_doctor.remove(db, id=doctor_id)

    return db_obj


@branches_router.get("/branches/", response_model=list[BaseBranch], status_code=status.HTTP_200_OK)
def get_branches_list(db: Session = Depends(get_db)):
    branches = crud_branch.get_multi(db)

    return branches


@branches_router.get("/branches/{branch_id}", response_model=BaseBranch, status_code=status.HTTP_200_OK)
def get_branches(branch_id: int, db: Session = Depends(get_db)):
    branches = crud_branch.get(db, id=branch_id)
    if branches is None:
        raise HTTPException(status_code=404, detail="Branch not fount")

    return branches


@branches_router.post("/branches/", response_model=CreateBranch, status_code=status.HTTP_201_CREATED)
def create_branch(obj_in: CreateBranch, db: Session = Depends(get_db)):
    branches = crud_branch.create(db, obj_in=obj_in)

    return branches


@branches_router.put("/branches/{branch_id}", response_model=BranchUpdate, status_code=status.HTTP_200_OK)
def branch_update(branch_id: int, obj_in: BranchUpdate, db: Session = Depends(get_db)):
    branches = crud_branch.get(db, branch_id)
    if branches is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    branches = crud_branch.update(db, db_obj=branches, obj_in=obj_in)

    return branches


@branches_router.delete("/branches/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    branches = crud_branch.get(db, branch_id)
    if branches is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    branches = crud_branch.remove(db, id=branch_id)

    return branches
