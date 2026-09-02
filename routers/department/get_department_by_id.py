from db_connection import LocalSession
from models import Department
from exceptions import DepartmentNotFoundException
from utils.logger import log_error

def get_department_by_id(department_id: int):
    session = LocalSession()
    try:
        dept = session.get(Department, department_id)
        if not dept:
            error_msg = f'Department with ID {department_id} not found.'
            log_error(f'DepartmentNotFoundException: {error_msg}')
            raise DepartmentNotFoundException(error_msg)
        return dept
    finally:
        session.close()
