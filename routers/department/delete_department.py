from db_connection import LocalSession
from models import Department
from exceptions import DepartmentNotFoundException
from utils.logger import log_activity, log_error

def delete_department(department_id: int):
    session = LocalSession()
    try:
        dept = session.get(Department, department_id)
        if not dept:
            error_msg = f'Department with ID {department_id} not found.'
            log_error(f'DepartmentNotFoundException: {error_msg}')
            raise DepartmentNotFoundException(error_msg)
        session.delete(dept)
        session.commit()
        log_activity(f'Department {department_id} deleted successfully')
        return {'message': f'Department {department_id} deleted successfully.'}
    except Exception as e:
        session.rollback()
        log_error(f'Error deleting department {department_id}: {str(e)}')
        raise e
    finally:
        session.close()
