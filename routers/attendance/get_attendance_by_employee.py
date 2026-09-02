from db_connection import LocalSession
from models import Attendance, Employee
from sqlalchemy import select
from exceptions import EmployeeNotFoundException
from utils.logger import log_error

def get_attendance_by_employee(employee_id: int):
    session = LocalSession()
    try:
        employee = session.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        return session.scalars(select(Attendance).where(Attendance.employee_id == employee_id).order_by(Attendance.attendance_date.desc())).all()
    finally:
        session.close()
