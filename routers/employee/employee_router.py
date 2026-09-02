from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from exceptions import EmployeeNotFoundException, InvalidDepartmentException, DatabaseOperationException
from routers.employee.create_employee import create_employee
from routers.employee.get_all_employees import get_all_employees
from routers.employee.get_employee_by_id import get_employee_by_id
from routers.employee.get_employees_by_department import get_employees_by_department
from routers.employee.update_employee import update_employee
from routers.employee.delete_employee import delete_employee

router = APIRouter(prefix='/employees', tags=['Employees'])

@router.post('', response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee_route(emp_data: EmployeeCreate):
    try:
        return create_employee(emp_data)
    except (InvalidDepartmentException, DatabaseOperationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('', response_model=List[EmployeeResponse])
def get_all_employees_route():
    return get_all_employees()

@router.get('/{employee_id}', response_model=EmployeeResponse)
def get_employee_by_id_route(employee_id: int):
    try:
        return get_employee_by_id(employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/department/{department_id}', response_model=List[EmployeeResponse])
def get_employees_by_department_route(department_id: int):
    try:
        return get_employees_by_department(department_id)
    except InvalidDepartmentException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put('/{employee_id}', response_model=EmployeeResponse)
def update_employee_route(employee_id: int, emp_data: EmployeeUpdate):
    try:
        return update_employee(employee_id, emp_data)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidDepartmentException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete('/{employee_id}')
def delete_employee_route(employee_id: int):
    try:
        return delete_employee(employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
