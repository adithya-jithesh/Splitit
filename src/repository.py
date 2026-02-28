from sqlalchemy.orm import Session
from src.models import LoanDB
from decimal import Decimal

def save_loan_to_db(db: Session, amount: Decimal, installments: int):
    # 1. Create the main Loan record
    new_loan = LoanDB(
        total_amount=amount,
        num_installments=installments,
        status="PENDING"
    )
    
    db.add(new_loan)
    db.commit()  # Save to get the ID
    db.refresh(new_loan) # Pull the ID back from the DB
    
    print(f"Loan {new_loan.loan_id} successfully carved into the database!")
    return new_loan