from db_connection import LocalSession
from models import Employee
from sqlalchemy import select
from routers.report.get_attendance_summary import get_attendance_summary

def get_low_attendance(threshold_percentage: float = 75.0):
    session = LocalSession()
    try:
        employees = session.scalars(select(Employee).order_by(Employee.employee_id)).all()
        low_attendance_list = []
        for emp in employees:
            summary = get_attendance_summary(emp.employee_id)
            if summary['working_days'] > 0 and summary['attendance_percentage'] < threshold_percentage:
                low_attendance_list.append(summary)
        return low_attendance_list
    finally:
        session.close()
