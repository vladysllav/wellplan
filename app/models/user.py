import enum


from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, Enum
from sqlalchemy.sql import func
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

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

