import os
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)

def write_file(filename: str, content: str) -> str:
    file_path = os.path.join(REPORTS_DIR, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    return file_path

def save_employee_report(content: str) -> str:
    return write_file('employee_report.txt', content)

def save_attendance_report(content: str) -> str:
    return write_file('attendance_report.txt', content)

def save_leave_report(content: str) -> str:
    return write_file('leave_report.txt', content)
