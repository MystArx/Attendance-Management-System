from pydantic import BaseModel
from datetime import date
from typing import Optional

class EmployeeCreate(BaseModel):
    employee_id: int
    employee_name: str
    email: str
    age: int
    gender: str
    salary: float
    joining_date: date
    department_id: int

class EmployeeUpdate(BaseModel):
    employee_name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    salary: Optional[float] = None
    department_id: Optional[int] = None

class EmployeeResponse(BaseModel):
    employee_id: int
    employee_name: str
    email: str
    age: int
    gender: str
    salary: float
    joining_date: date
    department_id: int

    class Config:
        from_attributes = True
