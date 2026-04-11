from .base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class Admin(Base):
    __tablename__ = "admin_table"

    id = Column(Integer, primary_key=True)
    job_number = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    hashed_password = Column(String)