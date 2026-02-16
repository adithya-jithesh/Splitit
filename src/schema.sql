CREATE TABLE loans (
    loan_id UUID PRIMERY KEY,
    total_amount DECIMAL(12, 2) NOT NULL,
    num_installments INTEAGER NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE installments (
    installment_id UUID PRIMERY KEY,
    loan_id UUID REFERENCES loans(loan_id),
    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
    amount DECIMAL(12, 2) Not NULL,
    status VARCHAR(20) DEFAULT 'SCHEDULED'
)