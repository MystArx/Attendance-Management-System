from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database_connection import get_db
from schemas.employee_schema import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from services.employee_service import EmployeeService
from exceptions.custom_exceptions import EmployeeNotFoundException, InvalidDepartmentException, DatabaseOperationException
from typing import List
router = APIRouter(prefix='/employees', tags=['Employees'])
employee_service = EmployeeService()

@router.post('', response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(emp_data: EmployeeCreate, db: Session=Depends(get_db)):
    try:
        return employee_service.add_employee(db, emp_data)
    except InvalidDepartmentException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('', response_model=List[EmployeeResponse])
def get_all_employees(db: Session=Depends(get_db)):
    return employee_service.get_all_employees(db)

@router.get('/{employee_id}', response_model=EmployeeResponse)
def get_employee_by_id(employee_id: int, db: Session=Depends(get_db)):
    try:
        return employee_service.search_employee(db, employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/department/{department_id}', response_model=List[EmployeeResponse])
def get_employees_by_department(department_id: int, db: Session=Depends(get_db)):
    try:
        return employee_service.get_employees_by_department(db, department_id)
    except InvalidDepartmentException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put('/{employee_id}', response_model=EmployeeResponse)
def update_employee(employee_id: int, emp_data: EmployeeUpdate, db: Session=Depends(get_db)):
    try:
        return employee_service.update_employee(db, employee_id, emp_data)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidDepartmentException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete('/{employee_id}')
def delete_employee(employee_id: int, db: Session=Depends(get_db)):
    try:
        return employee_service.delete_employee(db, employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
