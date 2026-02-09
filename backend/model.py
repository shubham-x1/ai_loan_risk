from pydantic import BaseModel
from typing import Optional

class LoanApplication(BaseModel):
    gender: str
    married: str
    dependents: str
    education: str
    self_employed: str
    applicant_income: int
    coapplicant_income: int
    loan_amount: int
    loan_amount_term: int
    credit_history: float
    property_area: str

class PredictionResponse(BaseModel):
    approved: bool
    approval_probability: float
    risk_score: float
    suggested_interest_rate: float
    fraud_flag: bool
    explanation: str
    application_id: Optional[str] = None