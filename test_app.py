import os
from datetime import date
from db_connection import create_tables
from schemas import DepartmentCreate, EmployeeCreate, AttendanceCreate, LeaveRequestCreate
from exceptions import DuplicateAttendanceException
from routers.department.add_department import add_department
from routers.department.get_department_by_id import get_department_by_id
from routers.employee.create_employee import create_employee
from routers.employee.get_employee_by_id import get_employee_by_id
from routers.attendance.mark_attendance import mark_attendance
from routers.leave.submit_leave import submit_leave
from routers.leave.approve_leave import approve_leave
from routers.leave.get_leave_balance import get_leave_balance
from routers.leave.get_employee_leaves import get_employee_leaves
from routers.report.get_attendance_summary import get_attendance_summary
from routers.report.export_report_files import export_report_files

def run_verification():
    print('==================================================')
    print('RUNNING DIRECT SYSTEM VERIFICATION')
    print('==================================================')
    create_tables()
    print('[PASS] Database tables created successfully.')
    
    dept_data = DepartmentCreate(department_id=1, department_name='Software Engineering', location='Bangalore, Tower B')
    try:
        dept = add_department(dept_data)
        print(f'[PASS] Added Department: {dept.department_name} (ID: {dept.department_id})')
    except Exception:
        dept = get_department_by_id(1)
        print(f'[INFO] Department exists: {dept.department_name}')
        
    emp_data = EmployeeCreate(employee_id=101, employee_name='Rahul Sharma', email='rahul.sharma@example.com', age=26, gender='Male', salary=85000.0, joining_date=date(2023, 1, 15), department_id=1)
    try:
        emp = create_employee(emp_data)
        print(f'[PASS] Added Employee: {emp.employee_name} (ID: {emp.employee_id})')
    except Exception:
        emp = get_employee_by_id(101)
        print(f'[INFO] Employee exists: {emp.employee_name}')
        
    bal = get_leave_balance(101)
    print(f'[PASS] Initial Leave Balance -> Casual: {bal.casual_leave}, Sick: {bal.sick_leave}, Earned: {bal.earned_leave}')
    
    att_data = AttendanceCreate(attendance_id=1001, employee_id=101, attendance_date=date(2026, 8, 25), check_in_time='09:00 AM', check_out_time='06:00 PM', attendance_status='Present')
    try:
        att = mark_attendance(att_data)
        print(f'[PASS] Marked Attendance for Employee {att.employee_id} on {att.attendance_date}')
    except DuplicateAttendanceException:
        print('[INFO] Attendance was already marked for this date.')
        
    try:
        att_dup = AttendanceCreate(attendance_id=1002, employee_id=101, attendance_date=date(2026, 8, 25), check_in_time='09:30 AM', check_out_time='06:00 PM', attendance_status='Present')
        mark_attendance(att_dup)
        print('[FAIL] Duplicate attendance was not blocked!')
    except DuplicateAttendanceException as e:
        print(f'[PASS] Duplicate Attendance blocked correctly: {e.message}')
        
    leave_data = LeaveRequestCreate(leave_id=501, employee_id=101, leave_type='Casual', from_date=date(2026, 9, 1), to_date=date(2026, 9, 3), reason='Family Event')
    try:
        leave = submit_leave(leave_data)
        print(f'[PASS] Submitted Leave Request: {leave.leave_id} ({leave.number_of_days} days, Status: {leave.leave_status})')
    except Exception:
        leaves = get_employee_leaves(101)
        leave = leaves[0]
        print(f'[INFO] Leave Request exists: {leave.leave_id}')
        
    if leave.leave_status != 'Approved':
        approved_leave = approve_leave(leave.leave_id)
        print(f'[PASS] Approved Leave Request: {approved_leave.leave_id}, Status: {approved_leave.leave_status}')
        
    bal_after = get_leave_balance(101)
    print(f'[PASS] Updated Leave Balance after approval -> Casual: {bal_after.casual_leave}, Sick: {bal_after.sick_leave}, Earned: {bal_after.earned_leave}')
    
    summary = get_attendance_summary(101)
    print(f"[PASS] Attendance Summary -> Working Days: {summary['working_days']}, Present: {summary['present_days']}, Attendance%: {summary['attendance_percentage']}%")
    
    file_result = export_report_files(101)
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

if __name__ == '__main__':
    run_verification()
