from db_connection import engine, Base
import models  

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    create_tables()
    print("Tables created successfully.")
