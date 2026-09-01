from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.database_connection import Base


class LeaveBalance(Base):
    __tablename__ = "leave_balance_table"

    leave_balance_id = Column(Integer, primary_key=True)
    
    # Foreign Key referencing employee_table.employee_id
    employee_id = Column(
        Integer,
        ForeignKey("employee_table.employee_id"),
        nullable=False,
        unique=True
    )
    
    casual_leave = Column(Integer, default=12)
    sick_leave = Column(Integer, default=10)
    earned_leave = Column(Integer, default=15)

    # Relationship back to Employee
    employee = relationship(
        "Employee",
        back_populates="leave_balance"
    )
