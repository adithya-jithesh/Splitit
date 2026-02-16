from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# In src/database.py
DATABASE_URL = "postgresql://adith_admin:splitit_password@127.0.0.1:5432/splitit_ledger"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()