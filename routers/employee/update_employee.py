from db_connection import LocalSession
from models import Employee, Department
from schemas import EmployeeUpdate
from exceptions import EmployeeNotFoundException, InvalidDepartmentException
from utils.logger import log_activity, log_error

def update_employee(employee_id: int, data: EmployeeUpdate):
    session = LocalSession()
    try:
        employee = session.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee with ID {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        if data.department_id is not None:
            dept = session.get(Department, data.department_id)
            if not dept:
                raise InvalidDepartmentException(f'Department {data.department_id} does not exist.')
            employee.department_id = data.department_id
        if data.employee_name is not None:
            employee.employee_name = data.employee_name
        if data.email is not None:
            employee.email = data.email
        if data.age is not None:
            employee.age = data.age
        if data.gender is not None:
            employee.gender = data.gender
        if data.salary is not None:
            employee.salary = data.salary
        session.commit()
        session.refresh(employee)
        log_activity(f'Employee {employee_id} updated successfully')
        return employee
    except Exception as e:
        session.rollback()
        log_error(f'Error updating employee {employee_id}: {str(e)}')
        raise e
    finally:
        session.close()
