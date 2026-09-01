from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.database_connection import Base

class Attendance(Base):
    __tablename__ = "attendance"
    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employee_table.employee_id"), nullable=False)
    attendance_date = Column(Date, nullable=False)
    check_in_time = Column(String(20), nullable=True)
    check_out_time = Column(String(20), nullable=True)
    attendance_status = Column(String(20), nullable=False)

    employee = relationship(
        "Employee",
        back_populates="attendances"
    )