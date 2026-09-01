from sqlalchemy.orm import Session
from sqlalchemy import select
from models.employee import Employee
from models.department import Department
from models.leave_balance import LeaveBalance
from schemas.employee_schema import EmployeeCreate, EmployeeUpdate
from exceptions.custom_exceptions import EmployeeNotFoundException, InvalidDepartmentException, DatabaseOperationException
from utils.logger import log_activity, log_error

class EmployeeService:

    def add_employee(self, db: Session, data: EmployeeCreate) -> Employee:
        try:
            dept = db.get(Department, data.department_id)
            if not dept:
                error_msg = f'Cannot add employee. Department {data.department_id} does not exist.'
                log_error(f'InvalidDepartmentException: {error_msg}')
                raise InvalidDepartmentException(error_msg)
            existing_emp = db.get(Employee, data.employee_id)
            if existing_emp:
                raise DatabaseOperationException(f'Employee with ID {data.employee_id} already exists.')
            new_employee = Employee(employee_id=data.employee_id, employee_name=data.employee_name, email=data.email, age=data.age, gender=data.gender, salary=data.salary, joining_date=data.joining_date, department_id=data.department_id)
            db.add(new_employee)
            default_leave_balance = LeaveBalance(employee_id=data.employee_id, casual_leave=12, sick_leave=10, earned_leave=15)
            db.add(default_leave_balance)
            db.commit()
            db.refresh(new_employee)
            log_activity(f'Employee {new_employee.employee_id} created successfully')
            return new_employee
        except Exception as e:
            db.rollback()
            log_error(f'Error adding employee: {str(e)}')
            raise e

    def get_all_employees(self, db: Session):
        employees = db.scalars(select(Employee).order_by(Employee.employee_id)).all()
        return employees

    def search_employee(self, db: Session, employee_id: int) -> Employee:
        employee = db.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee with ID {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        return employee

    def get_employees_by_department(self, db: Session, department_id: int):
        dept = db.get(Department, department_id)
        if not dept:
            error_msg = f'Department with ID {department_id} not found.'
            log_error(f'DepartmentNotFoundException: {error_msg}')
            raise InvalidDepartmentException(error_msg)
        employees = db.scalars(select(Employee).where(Employee.department_id == department_id).order_by(Employee.employee_id)).all()
        return employees

    def update_employee(self, db: Session, employee_id: int, data: EmployeeUpdate) -> Employee:
        employee = self.search_employee(db, employee_id)
        try:
            if data.department_id is not None:
                dept = db.get(Department, data.department_id)
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
            db.commit()
            db.refresh(employee)
            log_activity(f'Employee {employee_id} updated successfully')
            return employee
        except Exception as e:
            db.rollback()
            log_error(f'Error updating employee {employee_id}: {str(e)}')
            raise e

    def delete_employee(self, db: Session, employee_id: int):
        employee = self.search_employee(db, employee_id)
        try:
            db.delete(employee)
            db.commit()
            log_activity(f'Employee {employee_id} deleted successfully')
            return {'message': f'Employee {employee_id} deleted successfully.'}
        except Exception as e:
            db.rollback()
            log_error(f'Error deleting employee {employee_id}: {str(e)}')
            raise e
