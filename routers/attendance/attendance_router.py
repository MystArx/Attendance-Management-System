from datetime import date
from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import AttendanceCreate, AttendanceResponse
from exceptions import EmployeeNotFoundException, DuplicateAttendanceException, DatabaseOperationException
from routers.attendance.mark_attendance import mark_attendance
from routers.attendance.get_all_attendance import get_all_attendance
from routers.attendance.get_attendance_by_employee import get_attendance_by_employee
from routers.attendance.get_attendance_by_date import get_attendance_by_date

router = APIRouter(prefix='/attendance', tags=['Attendance'])

@router.post('', response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_attendance_route(attendance_data: AttendanceCreate):
    try:
        return mark_attendance(attendance_data)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (DuplicateAttendanceException, DatabaseOperationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('', response_model=List[AttendanceResponse])
def get_all_attendance_route():
    return get_all_attendance()

@router.get('/{employee_id}', response_model=List[AttendanceResponse])
def get_attendance_by_employee_route(employee_id: int):
    try:
        return get_attendance_by_employee(employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/date/{attendance_date}', response_model=List[AttendanceResponse])
def get_attendance_by_date_route(attendance_date: date):
    return get_attendance_by_date(attendance_date)
