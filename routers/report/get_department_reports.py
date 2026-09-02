from db_connection import LocalSession
from models import Department
from sqlalchemy import select

def get_department_reports():
    session = LocalSession()
    try:
        departments = session.scalars(select(Department).order_by(Department.department_id)).all()
        report_list = []
        for dept in departments:
            emp_list = [{'employee_id': emp.employee_id, 'employee_name': emp.employee_name, 'email': emp.email, 'salary': emp.salary} for emp in dept.employees]
            report_list.append({
                'department_id': dept.department_id,
                'department_name': dept.department_name,
                'location': dept.location,
                'total_employees': len(dept.employees),
                'employees': emp_list
            })
        return report_list
    finally:
        session.close()
