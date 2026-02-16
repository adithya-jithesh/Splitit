from sqlalchemy import Column, String, Numeric, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime, timedelta, timezone
from typing import List
import uuid
MIN_PURCHASE = Decimal('35.00')
MAX_PURCHASE = Decimal('5000.00')




@dataclass
class Installment:
    installment_id: str
    due_date: datetime
    amount: Decimal
    status: str = "SCHEDULED"



@dataclass
class SplitLoan:
    total_amount: Decimal
    num_installments: int = 4
    installments: List[Installment] = field(default_factory=list)
    loan_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)




class LoanDB(Base):
    __tablename__ = "loans"

    loan_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    total_amount = Column(Numeric, nullable=False)
    num_installments = Column(Integer, default=4)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    installments = relationship("InstallmentDB", back_populates="loan")




class InstallmentDB(Base):
    __tablename__ = "installments"

    installment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    loan_id = Column(String, ForeignKey("loans.loan_id"))
    amount = Column(Numeric, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(String, default="SCHEDULED")

    loan = relationship("LoanDB", back_populates="installments")
    

    
    
    def __post_init__(self):
        
        if self.total_amount < MIN_PURCHASE:
            raise ValueError(f"Amount ${self.total_amount} is too low for a split. Minimu is ${MIN_PURCHASE}.")
        if self.total_amount > MAX_PURCHASE:
            raise ValueError(f"Amount ${self.total_amount} exceeds the maximum allowed of ${MAX_PURCHASE}.")

    
    
    
    def get_allowed_terms(amount: Decimal) -> List[int]:
        if amount < Decimal('35.00'):
            return [1]
        elif amount < Decimal('500.00'):
            return[4]
        elif amount < Decimal('2000.00'):
            return [4, 8, 12]
        else:
            return [12, 24]
        

    
    
    
    def calculate_schedule(self):
        standard_payment = (self.total_amount / self.num_installments).quantize(Decimal('0.01'))

        total_from_standard = standard_payment * self.num_installments
        remainder = (self.total_amount - total_from_standard)

        for i in range(self.num_installments):

            amount_to_charge = standard_payment + (remainder if i == 0 else 0)

            due_date = self.created_at + timedelta(days=i *14)

            new_installment = Installment(
                installment_id=str(uuid.uuid4()),
                due_date=due_date,
                amount=amount_to_charge
            )

            self.installments.append(new_installment)

    
    
    def pay_next_installment(self) -> bool:
        
        for installment in self.installments:
            if installment.status == "SCHEDULED":
                installment.status = "PAID"
                print(f"Succesfully processed payment for installment ${installment.amount}")
                return True
        print("No pending installments to pay.")
        return False    
    