import logging
from datetime import datetime
import os


if not os.path.exists("logs"):
    os.makedirs("logs")


log_file = "logs/employee-management-" + \
           datetime.now().strftime("%Y-%m-%d") + ".log"


logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger("EmployeeProjectManagement")


logger.debug("Debug message - Detailed information")


logger.info("Info message - Application started")


logger.warning("Warning message - No employee found")


logger.error("Error message - Database operation failed")


logger.critical("Critical message - Application failure")