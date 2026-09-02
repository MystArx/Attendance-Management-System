from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from db_connection import create_tables
from routers import (
    department_router,
    employee_router,
    attendance_router,
    leave_router,
    report_router,
)
from exceptions import (
    EmployeeNotFoundException,
    DepartmentNotFoundException,
    InvalidDepartmentException,
    DuplicateAttendanceException,
    InsufficientLeaveBalanceException,
    LeaveRequestNotFoundException,
    DatabaseOperationException,
)
from utils.logger import log_activity, log_error

create_tables()
log_activity('Database tables verified/created successfully.')

app = FastAPI(
    title='Employee Leave & Attendance Management System',
    description='REST API matching employee_project_api structure.',
    version='1.0.0'
)

@app.exception_handler(EmployeeNotFoundException)
def employee_not_found_handler(request: Request, exc: EmployeeNotFoundException):
    log_error(f'EmployeeNotFoundException: {exc.message}')
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error_type': 'EmployeeNotFoundException', 'message': exc.message})

@app.exception_handler(DepartmentNotFoundException)
@app.exception_handler(InvalidDepartmentException)
def department_not_found_handler(request: Request, exc: Exception):
    message = getattr(exc, 'message', str(exc))
    log_error(f'DepartmentNotFoundException: {message}')
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error_type': 'DepartmentNotFoundException', 'message': message})

@app.exception_handler(DuplicateAttendanceException)
def duplicate_attendance_handler(request: Request, exc: DuplicateAttendanceException):
    log_error(f'DuplicateAttendanceException: {exc.message}')
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error_type': 'DuplicateAttendanceException', 'message': exc.message})

@app.exception_handler(InsufficientLeaveBalanceException)
def insufficient_leave_handler(request: Request, exc: InsufficientLeaveBalanceException):
    log_error(f'InsufficientLeaveBalanceException: {exc.message}')
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error_type': 'InsufficientLeaveBalanceException', 'message': exc.message})

@app.exception_handler(LeaveRequestNotFoundException)
def leave_not_found_handler(request: Request, exc: LeaveRequestNotFoundException):
    log_error(f'LeaveRequestNotFoundException: {exc.message}')
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error_type': 'LeaveRequestNotFoundException', 'message': exc.message})

@app.exception_handler(DatabaseOperationException)
def database_operation_handler(request: Request, exc: DatabaseOperationException):
    log_error(f'DatabaseOperationException: {exc.message}')
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'error_type': 'DatabaseOperationException', 'message': exc.message})

app.include_router(department_router)
app.include_router(employee_router)
app.include_router(attendance_router)
app.include_router(leave_router)
app.include_router(report_router)

@app.get('/')
def home():
    return {
        'project': 'Employee Leave & Attendance Management System',
        'status': 'Online',
        'documentation': '/docs',
        'version': '1.0.0',
        'message': 'Welcome to the Employee Management API. Visit /docs for Swagger UI.'
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
