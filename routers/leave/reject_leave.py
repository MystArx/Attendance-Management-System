from db_connection import LocalSession
from models import LeaveRequest
from exceptions import LeaveRequestNotFoundException
from utils.logger import log_activity, log_error

def reject_leave(leave_id: int):
    session = LocalSession()
    try:
        leave = session.get(LeaveRequest, leave_id)
        if not leave:
            error_msg = f'Leave request with ID {leave_id} not found.'
            log_error(f'LeaveRequestNotFoundException: {error_msg}')
            raise LeaveRequestNotFoundException(error_msg)
        leave.leave_status = 'Rejected'
        session.commit()
        session.refresh(leave)
        log_activity(f'Leave request {leave_id} rejected')
        return leave
    except Exception as e:
        session.rollback()
        log_error(f'Error rejecting leave request {leave_id}: {str(e)}')
        raise e
    finally:
        session.close()
