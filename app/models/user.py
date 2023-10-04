import enum
from sqlalchemy import Boolean, Column, Date, Enum, Integer, String

from app.db.base_class import Base
from app.models.base import TimestampedModel


class UserTypeEnum(enum.Enum):
    client = "client"
    admin = "admin"
    superadmin = "superadmin"


class User(TimestampedModel, Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    user_type = Column(Enum(UserTypeEnum), nullable=False, default=UserTypeEnum.client)
    date_of_birth = Column(Date(), nullable=False)

    @property
    def is_superuser(self) -> bool:
        return self.user_type == UserTypeEnum.superadmin
