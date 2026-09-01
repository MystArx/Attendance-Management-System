from sqlalchemy.orm import Session
from sqlalchemy import select
from models.employee import Employee
from models.department import Department
from models.attendance import Attendance
from models.leave_request import LeaveRequest
from models.leave_balance import LeaveBalance
from exceptions.custom_exceptions import EmployeeNotFoundException
from utils.logger import log_activity, log_error
from utils.file_handler import save_employee_report, save_attendance_report, save_leave_report

class ReportService:

    def generate_attendance_summary(self, db: Session, employee_id: int) -> dict:
        employee = db.get(Employee, employee_id)
        if not employee:
            error_msg = f'Employee with ID {employee_id} not found.'
            log_error(f'EmployeeNotFoundException: {error_msg}')
            raise EmployeeNotFoundException(error_msg)
        records = db.scalars(select(Attendance).where(Attendance.employee_id == employee_id)).all()
        total_working_days = len(records)
        present_days = sum((1 for r in records if r.attendance_status.lower() == 'present'))
        half_days = sum((1 for r in records if 'half' in r.attendance_status.lower()))
        absent_days = sum((1 for r in records if r.attendance_status.lower() == 'absent'))
        effective_present = present_days + half_days * 0.5
        attendance_percentage = round(effective_present / total_working_days * 100, 2) if total_working_days > 0 else 0.0
        dept_name = employee.department.department_name if employee.department else 'N/A'
        return {'employee_id': employee.employee_id, 'employee_name': employee.employee_name, 'department_name': dept_name, 'working_days': total_working_days, 'present_days': present_days, 'half_days': half_days, 'absent_days': absent_days, 'attendance_percentage': attendance_percentage}

    def generate_department_reports(self, db: Session):
        departments = db.scalars(select(Department).order_by(Department.department_id)).all()
        report_list = []
        for dept in departments:
            emp_list = [{'employee_id': emp.employee_id, 'employee_name': emp.employee_name, 'email': emp.email, 'salary': emp.salary} for emp in dept.employees]
            report_list.append({'department_id': dept.department_id, 'department_name': dept.department_name, 'location': dept.location, 'total_employees': len(dept.employees), 'employees': emp_list})
        return report_list

    def generate_employees_report(self, db: Session):
        employees = db.scalars(select(Employee).order_by(Employee.employee_id)).all()
        report_list = []
        for emp in employees:
            dept_name = emp.department.department_name if emp.department else 'N/A'
            balance = emp.leave_balance
            report_list.append({'employee_id': emp.employee_id, 'employee_name': emp.employee_name, 'email': emp.email, 'department': dept_name, 'salary': emp.salary, 'joining_date': str(emp.joining_date), 'leave_balance': {'casual_leave': balance.casual_leave if balance else 0, 'sick_leave': balance.sick_leave if balance else 0, 'earned_leave': balance.earned_leave if balance else 0}})
        return report_list

    def generate_low_attendance_report(self, db: Session, threshold_percentage: float=75.0):
        employees = db.scalars(select(Employee).order_by(Employee.employee_id)).all()
        low_attendance_list = []
        for emp in employees:
            summary = self.generate_attendance_summary(db, emp.employee_id)
            if summary['working_days'] > 0 and summary['attendance_percentage'] < threshold_percentage:
                low_attendance_list.append(summary)
        return low_attendance_list

    def export_all_report_files(self, db: Session, target_employee_id: int=None) -> dict:
        employees = db.scalars(select(Employee).order_by(Employee.employee_id)).all()
        emp_text = 'EMPLOYEE MASTER REPORT\n'
        emp_text += '======================\n\n'
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
        att_text = 'EMPLOYEE ATTENDANCE REPORT\n'
        att_text += '==========================\n\n'
        if target_employee_id:
            summary = self.generate_attendance_summary(db, target_employee_id)
            att_text += f"Employee ID: {summary['employee_id']}\n"
            att_text += f"Employee Name: {summary['employee_name']}\n"
            att_text += f"Department: {summary['department_name']}\n\n"
            att_text += f"Working Days: {summary['working_days']}\n"
            att_text += f"Present Days: {summary['present_days']}\n"
            att_text += f"Absent Days: {summary['absent_days']}\n"
            att_text += f"Attendance Percentage: {summary['attendance_percentage']}%\n"
        else:
            for emp in employees:
                summary = self.generate_attendance_summary(db, emp.employee_id)
                att_text += f"Employee ID: {summary['employee_id']}\n"
                att_text += f"Employee Name: {summary['employee_name']}\n"
                att_text += f"Department: {summary['department_name']}\n"
                att_text += f"Working Days: {summary['working_days']}\n"
                att_text += f"Present Days: {summary['present_days']}\n"
                att_text += f"Absent Days: {summary['absent_days']}\n"
                att_text += f"Attendance Percentage: {summary['attendance_percentage']}%\n"
                att_text += '----------------------------------------\n'
        att_path = save_attendance_report(att_text)
        leaves = db.scalars(select(LeaveRequest).order_by(LeaveRequest.leave_id.desc())).all()
        leave_text = 'EMPLOYEE LEAVE REPORT\n'
        leave_text += '=====================\n\n'
        for lr in leaves:
            emp = db.get(Employee, lr.employee_id)
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
        return {'message': 'Report files successfully generated and saved.', 'files': {'employee_report': emp_path, 'attendance_report': att_path, 'leave_report': leave_path}}
