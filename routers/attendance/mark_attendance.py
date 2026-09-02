from db_connection import LocalSession
from models import Attendance, Employee
from schemas import AttendanceCreate
from exceptions import EmployeeNotFoundException, DuplicateAttendanceException, DatabaseOperationException
from utils.logger import log_activity, log_error
from sqlalchemy import select

def mark_attendance(data: AttendanceCreate):
    session = LocalSession()
    try:
        employee = session.get(Employee, data.employee_id)
        if not employee:
            error_msg = f'Cannot mark attendance. Employee {data.employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        existing_record = session.scalars(
            select(Attendance).where(Attendance.employee_id == data.employee_id, Attendance.attendance_date == data.attendance_date)
        ).first()
        if existing_record:
            error_msg = f'Duplicate attendance: Employee {data.employee_id} already has attendance recorded for {data.attendance_date}.'
            log_error(f'DuplicateAttendanceException: {error_msg}')
            raise DuplicateAttendanceException(error_msg)
        existing_id = session.get(Attendance, data.attendance_id)
        if existing_id:
            raise DatabaseOperationException(f'Attendance ID {data.attendance_id} already exists.')
        new_attendance = Attendance(
            attendance_id=data.attendance_id,
            employee_id=data.employee_id,
            attendance_date=data.attendance_date,
            check_in_time=data.check_in_time,
            check_out_time=data.check_out_time,
            attendance_status=data.attendance_status
        )
        session.add(new_attendance)
        session.commit()
        session.refresh(new_attendance)
        log_activity(f'Employee {new_attendance.employee_id} attendance marked')
        return new_attendance
    except Exception as e:
        session.rollback()
        log_error(f'Error marking attendance: {str(e)}')
        raise e
    finally:
        session.close()
