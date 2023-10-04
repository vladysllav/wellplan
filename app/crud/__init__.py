# For a new basic set of CRUD operations you could just do

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

from .base import CRUDBase

user = CRUDBase[User, UserCreate, UserUpdate](User)
