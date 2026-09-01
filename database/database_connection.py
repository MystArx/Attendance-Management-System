from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL

# MySQL Database connection configuration
# Adjust username, password, host, port, and database as per your local MySQL setup
database_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="passs",  # Update with your MySQL password
    database="employee_project_db",
    host="localhost",
    port=3306
)

# Create the database engine
engine = create_engine(database_url, echo=False)

# Session factory bound to the engine
SessionLocal = sessionmaker(bind=engine)

# Declarative Base for ORM Models
Base = declarative_base()
