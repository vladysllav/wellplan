from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, Enum
from sqlalchemy.sql import func
from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    user_type = Column(Enum('client', 'admin', name='user_type_enum'))
    date_of_birth = Column(Date(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
