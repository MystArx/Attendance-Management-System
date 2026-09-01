from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database_connection import SessionLocal
from schemas.attendance_schema import AttendanceCreate, AttendanceResponse
from services.attendance_service import AttendanceService

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

attendance_service = AttendanceService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AttendanceResponse)
def mark_attendance(
    data: AttendanceCreate,
    db: Session = Depends(get_db)
):
    return attendance_service.mark_attendance(db, data)

@router.get("/", response_model=list[AttendanceResponse])
def get_all_attendance(
    db: Session = Depends(get_db)
):
    return attendance_service.get_all_attendance(db)

@router.get("/{employee_id}", response_model=list[AttendanceResponse])
def get_attendance_by_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    return attendance_service.get_attendance_by_employee(
        db,
        employee_id
    )