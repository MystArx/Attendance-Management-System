from db_connection import LocalSession
from models import Employee, Department, LeaveBalance
from schemas import EmployeeCreate
from exceptions import InvalidDepartmentException, DatabaseOperationException
from utils.logger import log_activity, log_error

def create_employee(data: EmployeeCreate):
    session = LocalSession()
    try:
        dept = session.get(Department, data.department_id)
        if not dept:
            error_msg = f'Cannot add employee. Department {data.department_id} does not exist.'
            log_error(f'InvalidDepartmentException: {error_msg}')
            raise InvalidDepartmentException(error_msg)
        existing_emp = session.get(Employee, data.employee_id)
        if existing_emp:
            raise DatabaseOperationException(f'Employee with ID {data.employee_id} already exists.')
        new_employee = Employee(
            employee_id=data.employee_id,
            employee_name=data.employee_name,
            email=data.email,
            age=data.age,
            gender=data.gender,
            salary=data.salary,
            joining_date=data.joining_date,
            department_id=data.department_id
        )
        session.add(new_employee)
        default_leave_balance = LeaveBalance(employee_id=data.employee_id, casual_leave=12, sick_leave=10, earned_leave=15)
        session.add(default_leave_balance)
        session.commit()
        session.refresh(new_employee)
        log_activity(f'Employee {new_employee.employee_id} created successfully')
        return new_employee
    except Exception as e:
        session.rollback()
        log_error(f'Error adding employee: {str(e)}')
        raise e
    finally:
        session.close()
