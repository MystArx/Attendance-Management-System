from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db_connection import Base

class Department(Base):
    __tablename__ = 'department_table'
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    employees = relationship('Employee', back_populates='department', cascade='all, delete-orphan')
