from db_connection import LocalSession
from models import Employee
from sqlalchemy import select

def get_employees_report():
    session = LocalSession()
    try:
        employees = session.scalars(select(Employee).order_by(Employee.employee_id)).all()
        report_list = []
        for emp in employees:
            dept_name = emp.department.department_name if emp.department else 'N/A'
            balance = emp.leave_balance
            report_list.append({
                'employee_id': emp.employee_id,
                'employee_name': emp.employee_name,
                'email': emp.email,
                'department': dept_name,
                'salary': emp.salary,
                'joining_date': str(emp.joining_date),
                'leave_balance': {
                    'casual_leave': balance.casual_leave if balance else 0,
                    'sick_leave': balance.sick_leave if balance else 0,
                    'earned_leave': balance.earned_leave if balance else 0
                }
            })
        return report_list
    finally:
        session.close()
