from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.base import CRUDBase
from app.models import Branch, Doctor
from app.schemas.doctor import (
    DoctorSchema,
    BaseBranch,
    BaseDoctor,
    BranchUpdate,
    CreateBranch,
    CreateDoctor,
    DoctorUpdate,
)

doctors_router = APIRouter()
branches_router = APIRouter()

crud_doctor = CRUDBase(Doctor)
crud_branch = CRUDBase(Branch)


@doctors_router.get(
    "/", response_model=list[DoctorSchema], status_code=status.HTTP_200_OK
)
def get_doctor_list(db: Session = Depends(get_db)):
    doctors = crud_doctor.get_multi(db)

    return doctors


@doctors_router.get(
    "/{doctor_id}", response_model=DoctorSchema, status_code=status.HTTP_200_OK
)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud_doctor.get(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor


# @doctors_router.post(
#     "/", response_model=CreateDoctor, status_code=status.HTTP_201_CREATED
# )
# def create_doctor(obj_in: CreateDoctor, db: Session = Depends(get_db)):
#     if not obj_in.branches:
#         raise HTTPException(status_code=400, detail="At least one branch must be provided")
#
#     doctor = crud_doctor.create(db, obj_in=obj_in)
#
#     for branch_id in obj_in.branches:
#         branch = crud_branch.get(db, branch_id)
#         if branch is None:
#             raise HTTPException(status_code=404, detail=f"Branch with id {branch_id} not found")
#
#         doctor.branches.append(branch)
#
#     db.commit()
#
#     return doctor


@doctors_router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_obj = crud_doctor.get(db, doctor_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db_obj = crud_doctor.remove(db, id=doctor_id)

    return db_obj


@doctors_router.patch("/{doctor_id}", response_model=BaseDoctor, status_code=status.HTTP_200_OK)
def patch_doctor(doctor_id: int, obj_in: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = crud_doctor.get(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Обновляем только переданные поля
    for field, value in obj_in.dict(exclude_unset=True).items():
        setattr(doctor, field, value)

    db.commit()
    db.refresh(doctor)
    return doctor


@branches_router.get(
    "/", response_model=list[BaseBranch], status_code=status.HTTP_200_OK
)
def get_branches_list(db: Session = Depends(get_db)):
    branches = crud_branch.get_multi(db)

    return branches


@branches_router.get(
    "/{branch_id}", response_model=BaseBranch, status_code=status.HTTP_200_OK
)
def get_branches(branch_id: int, db: Session = Depends(get_db)):
    branches = crud_branch.get(db, id=branch_id)
    if branches is None:
        raise HTTPException(status_code=404, detail="Branch not fount")

    return branches


@branches_router.post(
    "/", response_model=CreateBranch, status_code=status.HTTP_201_CREATED
)
def create_branch(obj_in: CreateBranch, db: Session = Depends(get_db)):
    branches = crud_branch.create(db, obj_in=obj_in)

    return branches


@branches_router.put(
    "/{branch_id}", response_model=BranchUpdate, status_code=status.HTTP_200_OK
)
def branch_update(branch_id: int, obj_in: BranchUpdate, db: Session = Depends(get_db)):
    branches = crud_branch.get(db, branch_id)
    if branches is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    branches = crud_branch.update(db, db_obj=branches, obj_in=obj_in)

    return branches


@branches_router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    branches = crud_branch.get(db, branch_id)
    if branches is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    branches = crud_branch.remove(db, id=branch_id)

    return branches
