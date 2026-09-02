from db_connection import LocalSession
from models import Employee
from exceptions import EmployeeNotFoundException
from utils.logger import log_activity, log_error

def delete_employee(employee_id: int):
    session = LocalSession()
    try:
        employee = session.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee with ID {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        session.delete(employee)
        session.commit()
        log_activity(f'Employee {employee_id} deleted successfully')
        return {'message': f'Employee {employee_id} deleted successfully.'}
    except Exception as e:
        session.rollback()
        log_error(f'Error deleting employee {employee_id}: {str(e)}')
        raise e
    finally:
        session.close()
