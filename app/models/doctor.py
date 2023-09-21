from sqlalchemy import Table, Column, Integer, ForeignKey, String, Date, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.base import TimestampedModel


doctor_branch_association = Table(
    "doctor_branch",
    Base.metadata,
    Column("doctor_id", Integer, ForeignKey("doctor.id")),
    Column("branch_id", Integer, ForeignKey("branch.id")),
)


class Doctor(TimestampedModel, Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)
    description = Column(Text)
    profile_image = Column(String, nullable=True)
    date_of_birth = Column(Date(), nullable=False)

    branches = relationship("Branch", secondary=doctor_branch_association, back_populates="doctors")


class Branch(TimestampedModel, Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)

    doctors = relationship("Doctor", secondary=doctor_branch_association, back_populates="branches")
