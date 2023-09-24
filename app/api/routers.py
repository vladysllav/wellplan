from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.auth import routes as auth_routes
from app.api.deps import get_db
from app.crud.base import CRUDBase
from app.models import Doctor, Branch

from app.schemas.doctor import CreateDoctor, DoctorUpdate, CreateBranch, BranchUpdate, BaseDoctor, BaseBranch

api_router = APIRouter()

api_router.include_router(auth_routes.router, prefix="/auth", tags=["auth"])


@api_router.post("/alive")
def alive() -> Any:
    """
    Default alive endpoint
    """
    return {"status": "ok"}


crud_doctor = CRUDBase(Doctor)
crud_branch = CRUDBase(Branch)


@api_router.post("/create_docs/", response_model=CreateDoctor, status_code=status.HTTP_201_CREATED)
def create_doctor(obj_in: CreateDoctor, db: Session = Depends(get_db)):
    doctor = crud_doctor.create(db, obj_in=obj_in)

    return doctor


@api_router.get("/doctors/", response_model=list[BaseDoctor], status_code=status.HTTP_200_OK)
def get_doctor_list(db: Session = Depends(get_db)):
    doctors = crud_doctor.get_multi(db)

    return doctors


@api_router.get("/doctors/{doctor_id}", response_model=BaseDoctor, status_code=status.HTTP_200_OK)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = crud_doctor.get(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor


@api_router.put("/update_doc/{doctor_id}", response_model=DoctorUpdate, status_code=status.HTTP_200_OK)
def update_doctor(doctor_id: int, obj_in: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = crud_doctor.get(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doctor = crud_doctor.update(db, db_obj=doctor, obj_in=obj_in)

    return doctor


@api_router.delete("/delete_doc/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_obj = crud_doctor.get(db, doctor_id)
    if db_obj is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db_obj = crud_doctor.remove(db, id=doctor_id)

    return db_obj


@api_router.get("/branches/", response_model=list[BaseBranch], status_code=status.HTTP_200_OK)
def get_branches_list(db: Session = Depends(get_db)):
    branches = crud_branch.get_multi(db)

    return branches


@api_router.get("/branches/{branch_id}", response_model=BaseBranch, status_code=status.HTTP_200_OK)
def get_branches(branch_id: int, db: Session = Depends(get_db)):
    branches = crud_branch.get(db, id=branch_id)
    if branches is None:
        raise HTTPException(status_code=404, detail="Branch not fount")

    return branches


@api_router.post("/create_branch/", response_model=CreateBranch, status_code=status.HTTP_201_CREATED)
def create_branch(obj_in: CreateBranch, db: Session = Depends(get_db)):
    branches = crud_branch.create(db, obj_in=obj_in)

    return branches


@api_router.put("/branches/{branch_id}", response_model=BranchUpdate, status_code=status.HTTP_200_OK)
def branch_update(branch_id: int, obj_in: BranchUpdate, db: Session = Depends(get_db)):
    branches = crud_branch.get(db, branch_id)
    if branches is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    branches = crud_branch.update(db, db_obj=branches, obj_in=obj_in)

    return branches


@api_router.delete("/branches/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    branches = crud_branch.get(db, branch_id)
    if branches is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    branches = crud_branch.remove(db, id=branch_id)

    return branches
