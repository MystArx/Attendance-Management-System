from fastapi import FastAPI
from database.database_connection import create_tables
from routers.attendance_router import router as attendance_router

create_tables()

app = FastAPI(title="Employee Leave & Attendance Management System")

app.include_router(attendance_router)