from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import LoanDB

app = FastAPI(title = "SplitIt BPNL API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return{"message": "Welcome to SplitIt API - Your Ledger is Online"}

@app.get("/loans")
def list_loans(db: Session = Depends(get_db)):
    loans = db.query(LoanDB).all()
    return loans