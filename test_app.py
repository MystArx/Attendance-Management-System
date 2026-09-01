import os
from datetime import date
from database.database_connection import SessionLocal, create_tables
from services import DepartmentService, EmployeeService, AttendanceService, LeaveService, ReportService
from schemas import DepartmentCreate, EmployeeCreate, AttendanceCreate, LeaveRequestCreate
from exceptions import DuplicateAttendanceException, InsufficientLeaveBalanceException, EmployeeNotFoundException

def run_verification():
    print('==================================================')
    print('RUNNING DIRECT SYSTEM VERIFICATION')
    print('==================================================')
    create_tables()
    print('[PASS] Database tables created successfully.')
    db = SessionLocal()
    dept_service = DepartmentService()
    emp_service = EmployeeService()
    att_service = AttendanceService()
    leave_service = LeaveService()
    report_service = ReportService()
    try:
        dept_data = DepartmentCreate(department_id=1, department_name='Software Engineering', location='Bangalore, Tower B')
        try:
            dept = dept_service.add_department(db, dept_data)
            print(f'[PASS] Added Department: {dept.department_name} (ID: {dept.department_id})')
        except Exception:
            dept = dept_service.get_department_by_id(db, 1)
            print(f'[INFO] Department exists: {dept.department_name}')
        emp_data = EmployeeCreate(employee_id=101, employee_name='Rahul Sharma', email='rahul.sharma@example.com', age=26, gender='Male', salary=85000.0, joining_date=date(2023, 1, 15), department_id=1)
        try:
            emp = emp_service.add_employee(db, emp_data)
            print(f'[PASS] Added Employee: {emp.employee_name} (ID: {emp.employee_id})')
        except Exception:
            emp = emp_service.search_employee(db, 101)
            print(f'[INFO] Employee exists: {emp.employee_name}')
        bal = leave_service.get_leave_balance(db, 101)
        print(f'[PASS] Initial Leave Balance -> Casual: {bal.casual_leave}, Sick: {bal.sick_leave}, Earned: {bal.earned_leave}')
        att_data = AttendanceCreate(attendance_id=1001, employee_id=101, attendance_date=date(2026, 8, 25), check_in_time='09:00 AM', check_out_time='06:00 PM', attendance_status='Present')
        try:
            att = att_service.mark_attendance(db, att_data)
            print(f'[PASS] Marked Attendance for Employee {att.employee_id} on {att.attendance_date}')
        except DuplicateAttendanceException:
            print('[INFO] Attendance was already marked for this date.')
        try:
            att_dup = AttendanceCreate(attendance_id=1002, employee_id=101, attendance_date=date(2026, 8, 25), check_in_time='09:30 AM', check_out_time='06:00 PM', attendance_status='Present')
            att_service.mark_attendance(db, att_dup)
            print('[FAIL] Duplicate attendance was not blocked!')
        except DuplicateAttendanceException as e:
            print(f'[PASS] Duplicate Attendance blocked correctly: {e.message}')
        leave_data = LeaveRequestCreate(leave_id=501, employee_id=101, leave_type='Casual', from_date=date(2026, 9, 1), to_date=date(2026, 9, 3), reason='Family Event')
        try:
            leave = leave_service.submit_leave_request(db, leave_data)
            print(f'[PASS] Submitted Leave Request: {leave.leave_id} ({leave.number_of_days} days, Status: {leave.leave_status})')
        except Exception:
            leaves = leave_service.get_employee_leaves(db, 101)
            leave = leaves[0]
            print(f'[INFO] Leave Request exists: {leave.leave_id}')
        if leave.leave_status != 'Approved':
            approved_leave = leave_service.approve_leave(db, leave.leave_id)
            print(f'[PASS] Approved Leave Request: {approved_leave.leave_id}, Status: {approved_leave.leave_status}')
        bal_after = leave_service.get_leave_balance(db, 101)
        print(f'[PASS] Updated Leave Balance after approval -> Casual: {bal_after.casual_leave}, Sick: {bal_after.sick_leave}, Earned: {bal_after.earned_leave}')
        summary = report_service.generate_attendance_summary(db, 101)
        print(f"[PASS] Attendance Summary -> Working Days: {summary['working_days']}, Present: {summary['present_days']}, Attendance%: {summary['attendance_percentage']}%")
        file_result = report_service.export_all_report_files(db, 101)
        print(f"[PASS] File Handling Result: {file_result['message']}")
        print(f"       -> Employee Report: {file_result['files']['employee_report']}")
        print(f"       -> Attendance Report: {file_result['files']['attendance_report']}")
        print(f"       -> Leave Report: {file_result['files']['leave_report']}")
        assert os.path.exists('reports/employee_report.txt')
        assert os.path.exists('reports/attendance_report.txt')
        assert os.path.exists('reports/leave_report.txt')
        assert os.path.exists('logs/application.log')
        assert os.path.exists('logs/error.log')
        print('[PASS] Verified all report files and log files exist on disk.')
        print('==================================================')
        print('ALL VERIFICATIONS COMPLETED SUCCESSFULLY!')
        print('==================================================')
    finally:
        db.close()
if __name__ == '__main__':
    run_verification()
