from db_connection import LocalSession
from models import Department
from sqlalchemy import select

def get_all_departments():
    session = LocalSession()
    try:
        return session.scalars(select(Department).order_by(Department.department_id)).all()
    finally:
        session.close()
