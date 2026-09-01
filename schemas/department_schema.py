from pydantic import BaseModel
from typing import Optional

class DepartmentCreate(BaseModel):
    department_id: int
    department_name: str
    location: str

class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    location: Optional[str] = None

class DepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    location: str

    class Config:
        from_attributes = True
