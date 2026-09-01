from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database_connection import get_db
from schemas.leave_schema import LeaveRequestCreate, LeaveRequestResponse, LeaveBalanceResponse
from services.leave_service import LeaveService
from exceptions.custom_exceptions import EmployeeNotFoundException, LeaveRequestNotFoundException, InsufficientLeaveBalanceException, DatabaseOperationException
from typing import List
router = APIRouter(tags=['Leaves'])
leave_service = LeaveService()

@router.post('/leaves', response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
def submit_leave(leave_data: LeaveRequestCreate, db: Session=Depends(get_db)):
    try:
        return leave_service.submit_leave_request(db, leave_data)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InsufficientLeaveBalanceException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/leaves', response_model=List[LeaveRequestResponse])
def get_all_leaves(db: Session=Depends(get_db)):
    return leave_service.get_all_leaves(db)

@router.get('/leaves/pending', response_model=List[LeaveRequestResponse])
def get_pending_leaves(db: Session=Depends(get_db)):
    return leave_service.get_pending_leaves(db)

@router.get('/leaves/employee/{employee_id}', response_model=List[LeaveRequestResponse])
def get_employee_leaves(employee_id: int, db: Session=Depends(get_db)):
    try:
        return leave_service.get_employee_leaves(db, employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put('/leaves/{leave_id}/approve', response_model=LeaveRequestResponse)
def approve_leave(leave_id: int, db: Session=Depends(get_db)):
    try:
        return leave_service.approve_leave(db, leave_id)
    except LeaveRequestNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put('/leaves/{leave_id}/reject', response_model=LeaveRequestResponse)
def reject_leave(leave_id: int, db: Session=Depends(get_db)):
    try:
        return leave_service.reject_leave(db, leave_id)
    except LeaveRequestNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/leave-balance/{employee_id}', response_model=LeaveBalanceResponse)
def get_leave_balance(employee_id: int, db: Session=Depends(get_db)):
    try:
        return leave_service.get_leave_balance(db, employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
