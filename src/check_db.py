from src.database import SessionLocal
from src.models import LoanDB

db = SessionLocal()
try:
    # Ask the database for ALL loans it has
    all_loans = db.query(LoanDB).all()
    
    print(f"Found {len(all_loans)} loans in the database.")
    for loan in all_loans:
        print(f"ID: {loan.loan_id} | Amount: ${loan.total_amount} | Status: {loan.status}")
        
        # We can even see the installments because of the 'relationship' we built!
        for i, inst in enumerate(loan.installments):
            print(f"  - Payment {i+1}: ${inst.amount} (Status: {inst.status})")
finally:
    db.close()