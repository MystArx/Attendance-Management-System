from sqlalchemy.orm import Session
from sqlalchemy import select
from models.department import Department
from schemas.department_schema import DepartmentCreate, DepartmentUpdate
from exceptions.custom_exceptions import DepartmentNotFoundException, DatabaseOperationException
from utils.logger import log_activity, log_error

class DepartmentService:

    def add_department(self, db: Session, data: DepartmentCreate) -> Department:
        try:
            existing_dept = db.get(Department, data.department_id)
            if existing_dept:
                raise DatabaseOperationException(f'Department with ID {data.department_id} already exists.')
            new_department = Department(department_id=data.department_id, department_name=data.department_name, location=data.location)
            db.add(new_department)
            db.commit()
            db.refresh(new_department)
            log_activity(f'Department {new_department.department_id} created successfully')
            return new_department
        except Exception as e:
            db.rollback()
            log_error(f'Error adding department: {str(e)}')
            raise e

    def get_all_departments(self, db: Session):
        departments = db.scalars(select(Department).order_by(Department.department_id)).all()
        return departments

    def get_department_by_id(self, db: Session, department_id: int) -> Department:
        dept = db.get(Department, department_id)
        if not dept:
            error_msg = f'Department with ID {department_id} not found.'
            log_error(f'DepartmentNotFoundException: {error_msg}')
            raise DepartmentNotFoundException(error_msg)
        return dept

    def update_department(self, db: Session, department_id: int, data: DepartmentUpdate) -> Department:
        dept = self.get_department_by_id(db, department_id)
        try:
            if data.department_name is not None:
                dept.department_name = data.department_name
            if data.location is not None:
                dept.location = data.location
            db.commit()
            db.refresh(dept)
            log_activity(f'Department {department_id} updated successfully')
            return dept
        except Exception as e:
            db.rollback()
            log_error(f'Error updating department {department_id}: {str(e)}')
            raise e

    def delete_department(self, db: Session, department_id: int):
        dept = self.get_department_by_id(db, department_id)
        try:
            db.delete(dept)
            db.commit()
            log_activity(f'Department {department_id} deleted successfully')
            return {'message': f'Department {department_id} deleted successfully.'}
        except Exception as e:
            db.rollback()
            log_error(f'Error deleting department {department_id}: {str(e)}')
            raise e
