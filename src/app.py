from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from decimal import Decimal
from src.repository import save_loan_to_db
from src.database import SessionLocal
from src.models import LoanDB

app = FastAPI(title="SplitIt BNPL API")

class LoanCreate(BaseModel):
    amount: float
    installments: int = 4

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

@app.post("/loans")
def make_new_loan(payload: LoanCreate, db: Session = Depends(get_db)):
    amount_dec = Decimal(str(payload.amount))
    new_loan = save_loan_to_db(db, amount_dec, payload.installments)
    return {"message" : "Loan Created","loan_id": str(new_loan.loan_id)}