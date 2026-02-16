from sqlalchemy.orm import Session
from src.models import LoanDB, InstallmentDB

def save_loan_to_db(db: Session, loan_data):

    new_loan = LoanDB(
        loan_id=loan_data['loan_id'],
        total_amount=loan_data['total_amount'],
        num_installments=len(loan_data['installments']),
    )

    db.add(new_loan)

    for inst in loan_data['installments']:
        new_inst = InstallmentDB(
            loan_id=new_loan.loan_id,
            amount=inst['amount'],
            due_date=inst['due_date'],
        )

        db.add(new_inst)

        db.commit()

    print(f"Loan {new_loan.loan_id} successfully carved into the database!")