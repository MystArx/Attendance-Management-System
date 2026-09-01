from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database_connection import get_db
from schemas.attendance_schema import AttendanceCreate, AttendanceResponse
from services.attendance_service import AttendanceService
from exceptions.custom_exceptions import EmployeeNotFoundException, DuplicateAttendanceException, DatabaseOperationException
from typing import List
router = APIRouter(prefix='/attendance', tags=['Attendance'])
attendance_service = AttendanceService()

@router.post('', response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_attendance(attendance_data: AttendanceCreate, db: Session=Depends(get_db)):
    try:
        return attendance_service.mark_attendance(db, attendance_data)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateAttendanceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('', response_model=List[AttendanceResponse])
def get_all_attendance(db: Session=Depends(get_db)):
    return attendance_service.get_all_attendance(db)

@router.get('/{employee_id}', response_model=List[AttendanceResponse])
def get_attendance_by_employee(employee_id: int, db: Session=Depends(get_db)):
    try:
        return attendance_service.get_attendance_by_employee(db, employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/date/{attendance_date}', response_model=List[AttendanceResponse])
def get_attendance_by_date(attendance_date: date, db: Session=Depends(get_db)):
    return attendance_service.get_attendance_by_date(db, attendance_date)
