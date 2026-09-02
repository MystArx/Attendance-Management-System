from db_connection import LocalSession
from models import LeaveBalance, Employee
from sqlalchemy import select
from exceptions import EmployeeNotFoundException
from utils.logger import log_error

def get_leave_balance(employee_id: int):
    session = LocalSession()
    try:
        employee = session.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        balance = session.scalars(select(LeaveBalance).where(LeaveBalance.employee_id == employee_id)).first()
        if not balance:
            balance = LeaveBalance(employee_id=employee_id, casual_leave=12, sick_leave=10, earned_leave=15)
            session.add(balance)
            session.commit()
            session.refresh(balance)
        return balance
    finally:
        session.close()
