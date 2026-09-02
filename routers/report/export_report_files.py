from db_connection import LocalSession
from models import Employee, LeaveRequest
from sqlalchemy import select
from utils.logger import log_activity
from utils.file_handler import save_employee_report, save_attendance_report, save_leave_report
from routers.report.get_attendance_summary import get_attendance_summary

def export_report_files(target_employee_id: int = None) -> dict:
    session = LocalSession()
    try:
        employees = session.scalars(select(Employee).order_by(Employee.employee_id)).all()
        emp_text = 'EMPLOYEE MASTER REPORT\n======================\n\n'
        for emp in employees:
            dept_name = emp.department.department_name if emp.department else 'N/A'
            balance = emp.leave_balance
            emp_text += f'Employee ID: {emp.employee_id}\n'
            emp_text += f'Name       : {emp.employee_name}\n'
            emp_text += f'Email      : {emp.email}\n'
            emp_text += f'Department : {dept_name}\n'
            emp_text += f'Salary     : ${emp.salary:,.2f}\n'
            emp_text += f'Joined     : {emp.joining_date}\n'
            if balance:
                emp_text += f'Leave Bal  : Casual={balance.casual_leave}, Sick={balance.sick_leave}, Earned={balance.earned_leave}\n'
            emp_text += '----------------------------------------\n'
        emp_path = save_employee_report(emp_text)

        att_text = 'EMPLOYEE ATTENDANCE REPORT\n==========================\n\n'
        if target_employee_id:
            summary = get_attendance_summary(target_employee_id)
            att_text += f"Employee ID: {summary['employee_id']}\n"
            att_text += f"Employee Name: {summary['employee_name']}\n"
            att_text += f"Department: {summary['department_name']}\n\n"
            att_text += f"Working Days: {summary['working_days']}\n"
            att_text += f"Present Days: {summary['present_days']}\n"
            att_text += f"Absent Days: {summary['absent_days']}\n"
            att_text += f"Attendance Percentage: {summary['attendance_percentage']}%\n"
        else:
            for emp in employees:
                summary = get_attendance_summary(emp.employee_id)
                att_text += f"Employee ID: {summary['employee_id']}\n"
                att_text += f"Employee Name: {summary['employee_name']}\n"
                att_text += f"Department: {summary['department_name']}\n"
                att_text += f"Working Days: {summary['working_days']}\n"
                att_text += f"Present Days: {summary['present_days']}\n"
                att_text += f"Absent Days: {summary['absent_days']}\n"
                att_text += f"Attendance Percentage: {summary['attendance_percentage']}%\n"
                att_text += '----------------------------------------\n'
        att_path = save_attendance_report(att_text)

        leaves = session.scalars(select(LeaveRequest).order_by(LeaveRequest.leave_id.desc())).all()
        leave_text = 'EMPLOYEE LEAVE REPORT\n=====================\n\n'
        for lr in leaves:
            emp = session.get(Employee, lr.employee_id)
            emp_name = emp.employee_name if emp else 'Unknown'
            leave_text += f'Leave ID   : {lr.leave_id}\n'
            leave_text += f'Employee   : {emp_name} (ID: {lr.employee_id})\n'
            leave_text += f'Type       : {lr.leave_type}\n'
            leave_text += f'Duration   : {lr.from_date} to {lr.to_date} ({lr.number_of_days} days)\n'
            leave_text += f'Status     : {lr.leave_status}\n'
            leave_text += f'Reason     : {lr.reason}\n'
            leave_text += '----------------------------------------\n'
        leave_path = save_leave_report(leave_text)

        log_activity('Employee report generated')
        return {
            'message': 'Report files successfully generated and saved.',
            'files': {
                'employee_report': emp_path,
                'attendance_report': att_path,
                'leave_report': leave_path
            }
        }
    finally:
        session.close()
