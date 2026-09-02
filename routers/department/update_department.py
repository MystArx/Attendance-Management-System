from db_connection import LocalSession
from models import Department
from schemas import DepartmentUpdate
from exceptions import DepartmentNotFoundException
from utils.logger import log_activity, log_error

def update_department(department_id: int, data: DepartmentUpdate):
    session = LocalSession()
    try:
        dept = session.get(Department, department_id)
        if not dept:
            error_msg = f'Department with ID {department_id} not found.'
            log_error(f'DepartmentNotFoundException: {error_msg}')
            raise DepartmentNotFoundException(error_msg)
        if data.department_name is not None:
            dept.department_name = data.department_name
        if data.location is not None:
            dept.location = data.location
        session.commit()
        session.refresh(dept)
        log_activity(f'Department {department_id} updated successfully')
        return dept
    except Exception as e:
        session.rollback()
        log_error(f'Error updating department {department_id}: {str(e)}')
        raise e
    finally:
        session.close()
