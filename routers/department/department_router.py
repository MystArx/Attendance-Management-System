from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from exceptions import DepartmentNotFoundException, DatabaseOperationException
from routers.department.add_department import add_department
from routers.department.get_all_departments import get_all_departments
from routers.department.get_department_by_id import get_department_by_id
from routers.department.update_department import update_department
from routers.department.delete_department import delete_department

router = APIRouter(prefix='/departments', tags=['Departments'])

@router.post('', response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(dept_data: DepartmentCreate):
    try:
        return add_department(dept_data)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('', response_model=List[DepartmentResponse])
def get_all_departments_route():
    return get_all_departments()

@router.get('/{department_id}', response_model=DepartmentResponse)
def get_department_by_id_route(department_id: int):
    try:
        return get_department_by_id(department_id)
    except DepartmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put('/{department_id}', response_model=DepartmentResponse)
def update_department_route(department_id: int, dept_data: DepartmentUpdate):
    try:
        return update_department(department_id, dept_data)
    except DepartmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete('/{department_id}')
def delete_department_route(department_id: int):
    try:
        return delete_department(department_id)
    except DepartmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
