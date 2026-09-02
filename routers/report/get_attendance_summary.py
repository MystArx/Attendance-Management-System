from db_connection import LocalSession
from models import Employee, Attendance
from sqlalchemy import select
from exceptions import EmployeeNotFoundException
from utils.logger import log_error

def get_attendance_summary(employee_id: int) -> dict:
    session = LocalSession()
    try:
        employee = session.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee with ID {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        records = session.scalars(select(Attendance).where(Attendance.employee_id == employee_id)).all()
        total_working_days = len(records)
        present_days = sum((1 for r in records if r.attendance_status.lower() == 'present'))
        half_days = sum((1 for r in records if 'half' in r.attendance_status.lower()))
        absent_days = sum((1 for r in records if r.attendance_status.lower() == 'absent'))
        effective_present = present_days + half_days * 0.5
        attendance_percentage = round(effective_present / total_working_days * 100, 2) if total_working_days > 0 else 0.0
        dept_name = employee.department.department_name if employee.department else 'N/A'
        return {
            'employee_id': employee.employee_id,
            'employee_name': employee.employee_name,
            'department_name': dept_name,
            'working_days': total_working_days,
            'present_days': present_days,
            'half_days': half_days,
            'absent_days': absent_days,
            'attendance_percentage': attendance_percentage
        }
    finally:
        session.close()
