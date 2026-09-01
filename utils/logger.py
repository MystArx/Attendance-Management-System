import os
import logging
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
APP_LOG_FILE = os.path.join(LOGS_DIR, 'application.log')
ERROR_LOG_FILE = os.path.join(LOGS_DIR, 'error.log')
app_logger = logging.getLogger('ApplicationLogger')
app_logger.setLevel(logging.INFO)
if not app_logger.handlers:
    app_handler = logging.FileHandler(APP_LOG_FILE, encoding='utf-8')
    app_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    app_handler.setFormatter(app_formatter)
    app_logger.addHandler(app_handler)
error_logger = logging.getLogger('ErrorLogger')
error_logger.setLevel(logging.ERROR)
if not error_logger.handlers:
    error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding='utf-8')
    error_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)

def log_activity(message: str):
    app_logger.info(message)
    print(f'[APP LOG] {message}')

def log_error(message: str):
    error_logger.error(message)
    print(f'[ERROR LOG] {message}')
