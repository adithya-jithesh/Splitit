from decimal import Decimal
# from src.models import SplitLoan
from src.database import SessionLocal
from src.repository import save_loan_to_db
from datetime import datetime, timedelta, timezone
import uuid

total_amount = Decimal('1200.00')
num_parts = 4
standard_payments = (total_amount / num_parts).quantize(Decimal('0.01'))

loan_data = {
    "loan_id": str(uuid.uuid4()),
    "total_amount": total_amount,
    "installments": []


}

for i in range (num_parts):
    loan_data["installments"].append({
        "amount": standard_payments,
        "due_date": datetime.now(timezone.utc) + timedelta(days=i * 14)
    })

db = SessionLocal()
try:
    save_loan_to_db(db, loan_data)
finally:
    db.close()