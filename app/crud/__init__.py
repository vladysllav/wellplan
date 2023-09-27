# For a new basic set of CRUD operations you could just do

from .base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

user = CRUDBase[User, UserCreate, UserUpdate](User)
