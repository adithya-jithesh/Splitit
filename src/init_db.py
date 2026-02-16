from src.database import engine, Base
from src.models import LoanDB, InstallmentDB

def create_tables():
    print("Connecting to database and creating tables...")

    Base.metadata.create_all(bind=engine)
print("Tables created successfully! Your 'Stone Tablet is ready.")

if __name__ == "__main__":
    create_tables()
    