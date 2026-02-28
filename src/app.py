from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from decimal import Decimal

from src.database import SessionLocal
from src.models import LoanDB

app = FastAPI(title="SplitIt BNPL API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to SplitIt API"}

@app.get("/loans")
def list_loans(db: Session = Depends(get_db)):
    return db.query(LoanDB).all()