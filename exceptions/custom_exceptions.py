class EmployeeNotFoundException(Exception):
    def __init__(self, message="Employee not found in the database."):
        self.message = message
        super().__init__(self.message)

class DepartmentNotFoundException(Exception):
    def __init__(self, message="Department not found in the database."):
        self.message = message
        super().__init__(self.message)

class InvalidDepartmentException(DepartmentNotFoundException):
    def __init__(self, message="Invalid department specified."):
        super().__init__(message)

class DuplicateAttendanceException(Exception):
    def __init__(self, message="Attendance already marked for this employee on this date."):
        self.message = message
        super().__init__(self.message)

class InsufficientLeaveBalanceException(Exception):
    def __init__(self, message="Insufficient leave balance for the requested leave type."):
        self.message = message
        super().__init__(self.message)

class LeaveRequestNotFoundException(Exception):
    def __init__(self, message="Leave request not found in the database."):
        self.message = message
        super().__init__(self.message)

class DatabaseOperationException(Exception):
    def __init__(self, message="Database operation failed."):
        self.message = message
        super().__init__(self.message)

