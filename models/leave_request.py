from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.database_connection import Base


class LeaveRequest(Base):
    __tablename__ = "leave_request_table"

    leave_id = Column(Integer, primary_key=True)
    
    # Foreign Key referencing employee_table.employee_id
    employee_id = Column(
        Integer,
        ForeignKey("employee_table.employee_id"),
        nullable=False
    )
    
    leave_type = Column(String(50), nullable=False)  # 'Casual', 'Sick', 'Earned'
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    number_of_days = Column(Integer, nullable=False)
    reason = Column(String(200), nullable=False)
    leave_status = Column(String(50), default="Pending")  # 'Pending', 'Approved', 'Rejected'

    # Relationship back to Employee
    employee = relationship(
        "Employee",
        back_populates="leave_requests"
    )
