from datetime import date
from pydantic import BaseModel


class BaseDoctor(BaseModel):
    first_name: str
    last_name: str
    experience: int
    email: str
    date_of_birth: date
    # branch_id: int


class DoctorUpdate(BaseDoctor):
    middle_name: str
    description: str
    profile_image: str


class CreateDoctor(BaseDoctor):
    pass


class Doctor(BaseDoctor):
    id: int

    class Config:
        orm_mode = True


class BaseBranch(BaseModel):
    title: str


class CreateBranch(BaseBranch):
    pass


class Branch(BaseBranch):
    id: int

    class Config:
        orm_mode = True


class BranchUpdate(BaseBranch):
    description: str
