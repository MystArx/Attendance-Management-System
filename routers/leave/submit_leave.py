from db_connection import LocalSession
from models import LeaveRequest, LeaveBalance, Employee
from schemas import LeaveRequestCreate
from exceptions import EmployeeNotFoundException, InsufficientLeaveBalanceException, DatabaseOperationException
from utils.logger import log_activity, log_error
from sqlalchemy import select

def submit_leave(data: LeaveRequestCreate):
    session = LocalSession()
    try:
        employee = session.get(Employee, data.employee_id)
        if not employee:
            error_msg = f'Cannot submit leave. Employee {data.employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        existing_leave = session.get(LeaveRequest, data.leave_id)
        if existing_leave:
            raise DatabaseOperationException(f'Leave Request with ID {data.leave_id} already exists.')
        if data.to_date < data.from_date:
            raise DatabaseOperationException("Leave 'to_date' cannot be earlier than 'from_date'.")
        number_of_days = (data.to_date - data.from_date).days + 1
        leave_balance = session.scalars(select(LeaveBalance).where(LeaveBalance.employee_id == data.employee_id)).first()
        if not leave_balance:
            leave_balance = LeaveBalance(employee_id=data.employee_id)
            session.add(leave_balance)
            session.commit()
            session.refresh(leave_balance)
        ltype = data.leave_type.strip().lower()
        if 'casual' in ltype:
            if leave_balance.casual_leave < number_of_days:
                error_msg = f'Insufficient Casual Leave balance. Requested: {number_of_days}, Available: {leave_balance.casual_leave}'
                log_error(f'InsufficientLeaveBalanceException: {error_msg}')
                raise InsufficientLeaveBalanceException(error_msg)
        elif 'sick' in ltype:
            if leave_balance.sick_leave < number_of_days:
                error_msg = f'Insufficient Sick Leave balance. Requested: {number_of_days}, Available: {leave_balance.sick_leave}'
                log_error(f'InsufficientLeaveBalanceException: {error_msg}')
                raise InsufficientLeaveBalanceException(error_msg)
        elif 'earned' in ltype:
            if leave_balance.earned_leave < number_of_days:
                error_msg = f'Insufficient Earned Leave balance. Requested: {number_of_days}, Available: {leave_balance.earned_leave}'
                log_error(f'InsufficientLeaveBalanceException: {error_msg}')
                raise InsufficientLeaveBalanceException(error_msg)
        else:
            raise DatabaseOperationException(f"Invalid leave type '{data.leave_type}'. Allowed: Casual, Sick, Earned.")
        new_leave = LeaveRequest(
            leave_id=data.leave_id,
            employee_id=data.employee_id,
            leave_type=data.leave_type,
            from_date=data.from_date,
            to_date=data.to_date,
            number_of_days=number_of_days,
            reason=data.reason,
            leave_status='Pending'
        )
        session.add(new_leave)
        session.commit()
        session.refresh(new_leave)
        log_activity(f'Leave request {new_leave.leave_id} submitted')
        return new_leave
    except Exception as e:
        session.rollback()
        log_error(f'Error submitting leave request: {str(e)}')
        raise e
    finally:
        session.close()
