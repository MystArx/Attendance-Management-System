from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database.database_connection import get_db
from services.report_service import ReportService
from exceptions.custom_exceptions import EmployeeNotFoundException
from typing import Optional
router = APIRouter(prefix='/reports', tags=['Reports & Analytics'])
report_service = ReportService()

@router.get('/attendance/{employee_id}')
def get_employee_attendance_summary(employee_id: int, db: Session=Depends(get_db)):
    try:
        return report_service.generate_attendance_summary(db, employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/departments')
def get_department_reports(db: Session=Depends(get_db)):
    return report_service.generate_department_reports(db)

@router.get('/employees')
def get_all_employees_report(db: Session=Depends(get_db)):
    return report_service.generate_employees_report(db)

@router.get('/low-attendance')
def get_low_attendance_employees(threshold_percentage: float=Query(75.0, description='Attendance threshold percentage'), db: Session=Depends(get_db)):
    return report_service.generate_low_attendance_report(db, threshold_percentage)

@router.post('/export-files')
def export_reports_to_files(employee_id: Optional[int]=Query(None, description='Optional employee ID for specific attendance report'), db: Session=Depends(get_db)):
    return report_service.export_all_report_files(db, employee_id)
