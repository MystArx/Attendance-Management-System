from sqlalchemy import Column, Integer, String
from database.database_connection import Base


class Department(Base):

    __tablename__ = "department"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(100), nullable=False, unique=True)
    location = Column(String(100), nullable=False)