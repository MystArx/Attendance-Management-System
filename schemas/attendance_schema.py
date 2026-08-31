from datetime import date
from typing import Optional
from pydantic import BaseModel

class AttendanceCreate(BaseModel):
    employee_id: int
    attendance_date: date
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    attendance_status: str

class AttendanceResponse(BaseModel):
    attendance_id: int
    employee_id: int
    attendance_date: date
    check_in_time: Optional[str]
    check_out_time: Optional[str]
    attendance_status: str

    class Config:
        from_attributes = True