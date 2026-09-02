from db_connection import LocalSession
from models import Department
from schemas import DepartmentCreate
from exceptions import DatabaseOperationException
from utils.logger import log_activity, log_error

def add_department(data: DepartmentCreate):
    session = LocalSession()
    try:
        existing_dept = session.get(Department, data.department_id)
        if existing_dept:
            raise DatabaseOperationException(f'Department with ID {data.department_id} already exists.')
        new_department = Department(department_id=data.department_id, department_name=data.department_name, location=data.location)
        session.add(new_department)
        session.commit()
        session.refresh(new_department)
        log_activity(f'Department {new_department.department_id} created successfully')
        return new_department
    except Exception as e:
        session.rollback()
        log_error(f'Error adding department: {str(e)}')
        raise e
    finally:
        session.close()
