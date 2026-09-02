from db_connection import LocalSession
from models import Employee
from sqlalchemy import select

def get_all_employees():
    session = LocalSession()
    try:
        return session.scalars(select(Employee).order_by(Employee.employee_id)).all()
    finally:
        session.close()
