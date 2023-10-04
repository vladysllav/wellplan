from datetime import date
from pydantic import BaseModel
from typing import Optional


class BaseDoctor(BaseModel):
    first_name: str
    last_name: str
    experience: int
    email: str
    date_of_birth: date
    # branch_id: int


class DoctorUpdate(BaseDoctor):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    experience: Optional[int] = None
    email: Optional[str] = None
    date_of_birth: Optional[date] = None
    middle_name: Optional[str] = None
    description: Optional[str] = None
    profile_image: Optional[str] = None


class CreateDoctor(BaseDoctor):
    pass


class DoctorSchema(BaseDoctor):
    id: int

    class Config:
        from_attributes = True


class BaseBranch(BaseModel):
    title: str


class CreateBranch(BaseBranch):
    pass


class Branch(BaseBranch):
    id: int

    class Config:
        from_attributes = True


class BranchUpdate(BaseBranch):
    description: str
