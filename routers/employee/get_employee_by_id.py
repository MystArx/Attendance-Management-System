from db_connection import LocalSession
from models import Employee
from exceptions import EmployeeNotFoundException
from utils.logger import log_error

def get_employee_by_id(employee_id: int):
    session = LocalSession()
    try:
        employee = session.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee with ID {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        return employee
    finally:
        session.close()
