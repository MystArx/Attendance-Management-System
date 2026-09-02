from db_connection import LocalSession
from models import LeaveRequest, Employee
from sqlalchemy import select
from exceptions import EmployeeNotFoundException
from utils.logger import log_error

def get_employee_leaves(employee_id: int):
    session = LocalSession()
    try:
        employee = session.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        return session.scalars(select(LeaveRequest).where(LeaveRequest.employee_id == employee_id).order_by(LeaveRequest.leave_id.desc())).all()
    finally:
        session.close()
