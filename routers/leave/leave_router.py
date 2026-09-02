from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import LeaveRequestCreate, LeaveRequestResponse, LeaveBalanceResponse
from exceptions import EmployeeNotFoundException, LeaveRequestNotFoundException, InsufficientLeaveBalanceException, DatabaseOperationException
from routers.leave.submit_leave import submit_leave
from routers.leave.get_all_leaves import get_all_leaves
from routers.leave.get_pending_leaves import get_pending_leaves
from routers.leave.get_employee_leaves import get_employee_leaves
from routers.leave.approve_leave import approve_leave
from routers.leave.reject_leave import reject_leave
from routers.leave.get_leave_balance import get_leave_balance

router = APIRouter(tags=['Leaves'])

@router.post('/leaves', response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
def submit_leave_route(leave_data: LeaveRequestCreate):
    try:
        return submit_leave(leave_data)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (InsufficientLeaveBalanceException, DatabaseOperationException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get('/leaves', response_model=List[LeaveRequestResponse])
def get_all_leaves_route():
    return get_all_leaves()

@router.get('/leaves/pending', response_model=List[LeaveRequestResponse])
def get_pending_leaves_route():
    return get_pending_leaves()

@router.get('/leaves/employee/{employee_id}', response_model=List[LeaveRequestResponse])
def get_employee_leaves_route(employee_id: int):
    try:
        return get_employee_leaves(employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put('/leaves/{leave_id}/approve', response_model=LeaveRequestResponse)
def approve_leave_route(leave_id: int):
    try:
        return approve_leave(leave_id)
    except LeaveRequestNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseOperationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put('/leaves/{leave_id}/reject', response_model=LeaveRequestResponse)
def reject_leave_route(leave_id: int):
    try:
        return reject_leave(leave_id)
    except LeaveRequestNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/leave-balance/{employee_id}', response_model=LeaveBalanceResponse)
def get_leave_balance_route(employee_id: int):
    try:
        return get_leave_balance(employee_id)
    except EmployeeNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
