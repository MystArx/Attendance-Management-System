from db_connection import LocalSession
from models import LeaveRequest
from sqlalchemy import select

def get_pending_leaves():
    session = LocalSession()
    try:
        return session.scalars(select(LeaveRequest).where(LeaveRequest.leave_status == 'Pending').order_by(LeaveRequest.leave_id)).all()
    finally:
        session.close()
