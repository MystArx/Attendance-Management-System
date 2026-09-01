from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database_connection import get_db
from schemas.department_schema import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from services.department_service import DepartmentService
from exceptions.custom_exceptions import DepartmentNotFoundException, DatabaseOperationException
from typing import List
router = APIRouter(prefix='/departments', tags=['Departments'])
department_service = DepartmentService()

@router.post('', response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(dept_data: DepartmentCreate, db: Session=Depends(get_db)):
    try:
        return department_service.add_department(db, dept_data)
    except DatabaseOperationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('', response_model=List[DepartmentResponse])
def get_all_departments(db: Session=Depends(get_db)):
    return department_service.get_all_departments(db)

@router.get('/{department_id}', response_model=DepartmentResponse)
def get_department_by_id(department_id: int, db: Session=Depends(get_db)):
    try:
        return department_service.get_department_by_id(db, department_id)
    except DepartmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put('/{department_id}', response_model=DepartmentResponse)
def update_department(department_id: int, dept_data: DepartmentUpdate, db: Session=Depends(get_db)):
    try:
        return department_service.update_department(db, department_id, dept_data)
    except DepartmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete('/{department_id}')
def delete_department(department_id: int, db: Session=Depends(get_db)):
    try:
        return department_service.delete_department(db, department_id)
    except DepartmentNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
