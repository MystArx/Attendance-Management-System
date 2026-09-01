from pydantic import BaseModel
from datetime import date
from typing import Optional

class LeaveRequestCreate(BaseModel):
    leave_id: int
    employee_id: int
    leave_type: str
    from_date: date
    to_date: date
    reason: str

class LeaveRequestResponse(BaseModel):
    leave_id: int
    employee_id: int
    leave_type: str
    from_date: date
    to_date: date
    number_of_days: int
    reason: str
    leave_status: str

    class Config:
        from_attributes = True

class LeaveBalanceResponse(BaseModel):
    leave_balance_id: int
    employee_id: int
    casual_leave: int
    sick_leave: int
    earned_leave: int

    class Config:
        from_attributes = True
