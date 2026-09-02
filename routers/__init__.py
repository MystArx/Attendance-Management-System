from routers.department.department_router import router as department_router
from routers.employee.employee_router import router as employee_router
from routers.attendance.attendance_router import router as attendance_router
from routers.leave.leave_router import router as leave_router
from routers.report.report_router import router as report_router

__all__ = ['department_router', 'employee_router', 'attendance_router', 'leave_router', 'report_router']
