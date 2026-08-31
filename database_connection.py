from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

database_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="coforge25",
    host="localhost",
    database="EmployeeProjectDB"
)

engine = create_engine(database_url)

SessionLocal = sessionmaker(bind=engine)