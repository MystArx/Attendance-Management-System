from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.attendance import Attendance
from models.employee import Employee
from schemas.attendance_schema import AttendanceCreate
from exceptions.custom_exceptions import (
    EmployeeNotFoundException,
    DuplicateAttendanceException,
    DatabaseOperationException
)
from utils.logger import log_activity, log_error


class AttendanceService:
    """Service class for handling all Attendance-related business operations."""

    def mark_attendance(self, db: Session, data: AttendanceCreate) -> Attendance:
        try:
            # 1. Validate employee exists
            employee = db.get(Employee, data.employee_id)
            if not employee:
                error_msg = f"Cannot mark attendance. Employee {data.employee_id} not found."
                log_error(f"EmployeeNotFoundException: {error_msg}")
                raise EmployeeNotFoundException(error_msg)

            # 2. Check if attendance already exists for this employee on this date (Requirement 9)
            existing_record = db.scalars(
                select(Attendance).where(
                    Attendance.employee_id == data.employee_id,
                    Attendance.attendance_date == data.attendance_date
                )
            ).first()

            if existing_record:
                error_msg = f"Duplicate attendance: Employee {data.employee_id} already has attendance recorded for {data.attendance_date}."
                log_error(f"DuplicateAttendanceException: {error_msg}")
                raise DuplicateAttendanceException(error_msg)

            # Check if attendance_id is already used
            existing_id = db.get(Attendance, data.attendance_id)
            if existing_id:
                raise DatabaseOperationException(f"Attendance ID {data.attendance_id} already exists.")

            # 3. Create attendance record
            new_attendance = Attendance(
                attendance_id=data.attendance_id,
                employee_id=data.employee_id,
                attendance_date=data.attendance_date,
                check_in_time=data.check_in_time,
                check_out_time=data.check_out_time,
                attendance_status=data.attendance_status
            )
            db.add(new_attendance)
            db.commit()
            db.refresh(new_attendance)

            log_activity(f"Employee {new_attendance.employee_id} attendance marked")
            return new_attendance

        except Exception as e:
            db.rollback()
            log_error(f"Error marking attendance: {str(e)}")
            raise e

    def get_all_attendance(self, db: Session):
        records = db.scalars(select(Attendance).order_by(Attendance.attendance_date.desc())).all()
        return records

    def get_attendance_by_employee(self, db: Session, employee_id: int):
        # Validate employee exists
        employee = db.get(Employee, employee_id)
        if not employee:
            error_msg = f"Employee {employee_id} not found."
            log_error(f"EmployeeNotFoundException: {error_msg}")
            raise EmployeeNotFoundException(error_msg)

        records = db.scalars(
            select(Attendance).where(Attendance.employee_id == employee_id).order_by(Attendance.attendance_date.desc())
        ).all()
        return records

    def get_attendance_by_date(self, db: Session, target_date: date):
        records = db.scalars(
            select(Attendance).where(Attendance.attendance_date == target_date).order_by(Attendance.employee_id)
        ).all()
        return records
