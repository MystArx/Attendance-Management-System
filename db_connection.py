from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = 'mysql+pymysql://root:password@localhost:3306/employee_management_db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
LocalSession = SessionLocal  
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
