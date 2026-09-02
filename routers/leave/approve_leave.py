from db_connection import LocalSession
from models import LeaveRequest, LeaveBalance
from sqlalchemy import select
from exceptions import LeaveRequestNotFoundException, DatabaseOperationException
from utils.logger import log_activity, log_error

def approve_leave(leave_id: int):
    session = LocalSession()
    try:
        leave = session.get(LeaveRequest, leave_id)
        if not leave:
            error_msg = f'Leave request with ID {leave_id} not found.'
            log_error(f'LeaveRequestNotFoundException: {error_msg}')
            raise LeaveRequestNotFoundException(error_msg)
        if leave.leave_status == 'Approved':
            return leave
        leave_balance = session.scalars(select(LeaveBalance).where(LeaveBalance.employee_id == leave.employee_id)).first()
        if not leave_balance:
            raise DatabaseOperationException(f'Leave balance record not found for employee {leave.employee_id}')
        ltype = leave.leave_type.strip().lower()
        if 'casual' in ltype:
            leave_balance.casual_leave -= leave.number_of_days
        elif 'sick' in ltype:
            leave_balance.sick_leave -= leave.number_of_days
        elif 'earned' in ltype:
            leave_balance.earned_leave -= leave.number_of_days
        leave.leave_status = 'Approved'
        session.commit()
        session.refresh(leave)
        log_activity(f'Leave request {leave_id} approved')
        return leave
    except Exception as e:
        session.rollback()
        log_error(f'Error approving leave request {leave_id}: {str(e)}')
        raise e
    finally:
        session.close()
