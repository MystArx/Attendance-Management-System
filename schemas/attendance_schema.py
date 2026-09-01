from pydantic import BaseModel
from datetime import date
from typing import Optional

class AttendanceCreate(BaseModel):
    attendance_id: int
    employee_id: int
    attendance_date: date
    check_in_time: Optional[str] = '09:00 AM'
    check_out_time: Optional[str] = '06:00 PM'
    attendance_status: str = 'Present'

class AttendanceResponse(BaseModel):
    attendance_id: int
    employee_id: int
    attendance_date: date
    check_in_time: Optional[str]
    check_out_time: Optional[str]
    attendance_status: str

    class Config:
        from_attributes = True
