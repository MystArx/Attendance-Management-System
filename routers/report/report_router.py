from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from exceptions import EmployeeNotFoundException
from routers.report.get_attendance_summary import get_attendance_summary
from routers.report.get_department_reports import get_department_reports
from routers.report.get_employees_report import get_employees_report
from routers.report.get_low_attendance import get_low_attendance
from routers.report.export_report_files import export_report_files

router = APIRouter(prefix='/reports', tags=['Reports & Analytics'])

@router.get('/attendance/{employee_id}')
def get_employee_attendance_summary_route(employee_id: int):
    try:
        return get_attendance_summary(employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/departments')
def get_department_reports_route():
    return get_department_reports()

@router.get('/employees')
def get_all_employees_report_route():
    return get_employees_report()

@router.get('/low-attendance')
def get_low_attendance_employees_route(threshold_percentage: float = Query(75.0, description='Attendance threshold percentage')):
    return get_low_attendance(threshold_percentage)

@router.post('/export-files')
def export_reports_to_files_route(employee_id: Optional[int] = Query(None, description='Optional employee ID for specific attendance report')):
    return export_report_files(employee_id)
