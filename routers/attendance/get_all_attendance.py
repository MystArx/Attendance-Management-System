from db_connection import LocalSession
from models import Attendance
from sqlalchemy import select

def get_all_attendance():
    session = LocalSession()
    try:
        return session.scalars(select(Attendance).order_by(Attendance.attendance_date.desc())).all()
    finally:
        session.close()
