from pydantic import BaseModel
from typing import List, Optional

class ReceiptItem(BaseModel):
    description: str
    amount: float

class FraudData(BaseModel):
    fraud_detected: bool
    fraud_type: Optional[str] = None  # Type of fraud if detected, e.g., "duplicate", "suspicious"

class ReceiptData(BaseModel):
    fraud_check: Optional[List[FraudData]] = False  # Optional field for fraud detection
    merchant: str
    date: str  
    total_amount: float
    items: Optional[List[ReceiptItem]] = None



class FeeItem(BaseModel):
    bill_date: Optional[str] = None  # Some bills may not have per-item date
    description: str
    amount: float
    bill_month: Optional[str] = None  # Some bills may not have a billing month

class ChildFeeForm(BaseModel):
    items: List[FeeItem]
    total: float  # Calculated after parsing




class MedicalClaimItem(BaseModel):
    name: str  # Patient name
    relationship: str  # self, spouse, parent, child
    category: str  # in-patient, out-patient, maternity(cesarean), maternity(normal)
    detail: str  # doctor's fee, diagnostic tests, medicines, other hospitalization
    amount: float

class MedicalReimbursementForm(BaseModel):
    company: Optional[str] = None
    extension_no: Optional[str] = None
    employee_name: str
    employee_code: str
    department: Optional[str] = None
    designation: Optional[str] = None
    date: Optional[str] = None
    billing_month: Optional[str] = None
    claims: List[MedicalClaimItem]
    total: float