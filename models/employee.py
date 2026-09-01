from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.database_connection import Base

class Employee(Base):
    __tablename__ = 'employee_table'
    employee_id = Column(Integer, primary_key=True)
    employee_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    salary = Column(Float, nullable=False)
    joining_date = Column(Date, nullable=False)
    department_id = Column(Integer, ForeignKey('department_table.department_id'), nullable=False)
    department = relationship('Department', back_populates='employees')
    attendances = relationship('Attendance', back_populates='employee', cascade='all, delete-orphan')
    leave_requests = relationship('LeaveRequest', back_populates='employee', cascade='all, delete-orphan')
    leave_balance = relationship('LeaveBalance', back_populates='employee', uselist=False, cascade='all, delete-orphan')
