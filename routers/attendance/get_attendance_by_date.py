from db_connection import LocalSession
from models import Attendance
from sqlalchemy import select
from datetime import date

def get_attendance_by_date(target_date: date):
    session = LocalSession()
    try:
        return session.scalars(select(Attendance).where(Attendance.attendance_date == target_date).order_by(Attendance.employee_id)).all()
    finally:
        session.close()
