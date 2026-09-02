from db_connection import LocalSession
from models import LeaveRequest
from sqlalchemy import select

def get_all_leaves():
    session = LocalSession()
    try:
        return session.scalars(select(LeaveRequest).order_by(LeaveRequest.leave_id.desc())).all()
    finally:
        session.close()
