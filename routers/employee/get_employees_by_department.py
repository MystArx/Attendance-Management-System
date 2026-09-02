from db_connection import LocalSession
from models import Employee, Department
from sqlalchemy import select
from exceptions import InvalidDepartmentException
from utils.logger import log_error

def get_employees_by_department(department_id: int):
    session = LocalSession()
    try:
        dept = session.get(Department, department_id)
        if not dept:
            error_msg = f'Department with ID {department_id} not found.'
            log_error(f'DepartmentNotFoundException: {error_msg}')
            raise InvalidDepartmentException(error_msg)
        return session.scalars(select(Employee).where(Employee.department_id == department_id).order_by(Employee.employee_id)).all()
    finally:
        session.close()
