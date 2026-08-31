from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "sqlite:///./employee_system.db"

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    """ Dependency function to provide a database session for FastAPI endpoints. Ensures the session is automatically closed after the request is finished. """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """ Creates all database tables defined by SQLAlchemy models. """
    Base.metadata.create_all(bind=engine)
