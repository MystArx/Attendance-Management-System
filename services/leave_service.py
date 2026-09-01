from sqlalchemy.orm import Session
from sqlalchemy import select
from models.leave_request import LeaveRequest
from models.leave_balance import LeaveBalance
from models.employee import Employee
from schemas.leave_schema import LeaveRequestCreate
from exceptions.custom_exceptions import EmployeeNotFoundException, LeaveRequestNotFoundException, InsufficientLeaveBalanceException, DatabaseOperationException
from utils.logger import log_activity, log_error

class LeaveService:

    def submit_leave_request(self, db: Session, data: LeaveRequestCreate) -> LeaveRequest:
        try:
            employee = db.get(Employee, data.employee_id)
            if not employee:
                error_msg = f'Cannot submit leave. Employee {data.employee_id} not found.'
                log_error(f'EmployeeNotFoundException: {error_msg}')
                raise EmployeeNotFoundException(error_msg)
            existing_leave = db.get(LeaveRequest, data.leave_id)
            if existing_leave:
                raise DatabaseOperationException(f'Leave Request with ID {data.leave_id} already exists.')
            if data.to_date < data.from_date:
                raise DatabaseOperationException("Leave 'to_date' cannot be earlier than 'from_date'.")
            number_of_days = (data.to_date - data.from_date).days + 1
            leave_balance = db.scalars(select(LeaveBalance).where(LeaveBalance.employee_id == data.employee_id)).first()
            if not leave_balance:
                leave_balance = LeaveBalance(employee_id=data.employee_id)
                db.add(leave_balance)
                db.commit()
                db.refresh(leave_balance)
            ltype = data.leave_type.strip().lower()
            if 'casual' in ltype:
                if leave_balance.casual_leave < number_of_days:
                    error_msg = f'Insufficient Casual Leave balance. Requested: {number_of_days}, Available: {leave_balance.casual_leave}'
                    log_error(f'InsufficientLeaveBalanceException: {error_msg}')
                    raise InsufficientLeaveBalanceException(error_msg)
            elif 'sick' in ltype:
                if leave_balance.sick_leave < number_of_days:
                    error_msg = f'Insufficient Sick Leave balance. Requested: {number_of_days}, Available: {leave_balance.sick_leave}'
                    log_error(f'InsufficientLeaveBalanceException: {error_msg}')
                    raise InsufficientLeaveBalanceException(error_msg)
            elif 'earned' in ltype:
                if leave_balance.earned_leave < number_of_days:
                    error_msg = f'Insufficient Earned Leave balance. Requested: {number_of_days}, Available: {leave_balance.earned_leave}'
                    log_error(f'InsufficientLeaveBalanceException: {error_msg}')
                    raise InsufficientLeaveBalanceException(error_msg)
            else:
                raise DatabaseOperationException(f"Invalid leave type '{data.leave_type}'. Allowed: Casual, Sick, Earned.")
            new_leave = LeaveRequest(leave_id=data.leave_id, employee_id=data.employee_id, leave_type=data.leave_type, from_date=data.from_date, to_date=data.to_date, number_of_days=number_of_days, reason=data.reason, leave_status='Pending')
            db.add(new_leave)
            db.commit()
            db.refresh(new_leave)
            log_activity(f'Leave request {new_leave.leave_id} submitted')
            return new_leave
        except Exception as e:
            db.rollback()
            log_error(f'Error submitting leave request: {str(e)}')
            raise e

    def get_all_leaves(self, db: Session):
        leaves = db.scalars(select(LeaveRequest).order_by(LeaveRequest.leave_id.desc())).all()
        return leaves

    def get_pending_leaves(self, db: Session):
        leaves = db.scalars(select(LeaveRequest).where(LeaveRequest.leave_status == 'Pending').order_by(LeaveRequest.leave_id)).all()
        return leaves

    def get_employee_leaves(self, db: Session, employee_id: int):
        employee = db.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        leaves = db.scalars(select(LeaveRequest).where(LeaveRequest.employee_id == employee_id).order_by(LeaveRequest.leave_id.desc())).all()
        return leaves

    def approve_leave(self, db: Session, leave_id: int) -> LeaveRequest:
        leave = db.get(LeaveRequest, leave_id)
        if not leave:
            error_msg = f'Leave request with ID {leave_id} not found.'
            log_error(f'LeaveRequestNotFoundException: {error_msg}')
            raise LeaveRequestNotFoundException(error_msg)
        if leave.leave_status == 'Approved':
            return leave
        try:
            leave_balance = db.scalars(select(LeaveBalance).where(LeaveBalance.employee_id == leave.employee_id)).first()
            if not leave_balance:
                raise DatabaseOperationException(f'Leave balance record not found for employee {leave.employee_id}')
            ltype = leave.leave_type.strip().lower()
            if 'casual' in ltype:
                leave_balance.casual_leave -= leave.number_of_days
            elif 'sick' in ltype:
                leave_balance.sick_leave -= leave.number_of_days
            elif 'earned' in ltype:
                leave_balance.earned_leave -= leave.number_of_days
            leave.leave_status = 'Approved'
            db.commit()
            db.refresh(leave)
            log_activity(f'Leave request {leave_id} approved')
            return leave
        except Exception as e:
            db.rollback()
            log_error(f'Error approving leave request {leave_id}: {str(e)}')
            raise e

    def reject_leave(self, db: Session, leave_id: int) -> LeaveRequest:
        leave = db.get(LeaveRequest, leave_id)
        if not leave:
            error_msg = f'Leave request with ID {leave_id} not found.'
            log_error(f'LeaveRequestNotFoundException: {error_msg}')
            raise LeaveRequestNotFoundException(error_msg)
        try:
            leave.leave_status = 'Rejected'
            db.commit()
            db.refresh(leave)
            log_activity(f'Leave request {leave_id} rejected')
            return leave
        except Exception as e:
            db.rollback()
            log_error(f'Error rejecting leave request {leave_id}: {str(e)}')
            raise e

    def get_leave_balance(self, db: Session, employee_id: int) -> LeaveBalance:
        employee = db.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        balance = db.scalars(select(LeaveBalance).where(LeaveBalance.employee_id == employee_id)).first()
        if not balance:
            balance = LeaveBalance(employee_id=employee_id, casual_leave=12, sick_leave=10, earned_leave=15)
            db.add(balance)
            db.commit()
            db.refresh(balance)
        return balance
