from pydantic import BaseModel
from typing import List, Optional

class ReceiptItem(BaseModel):
    description: str
    amount: float

class ReceiptData(BaseModel):
    fraud_check: Optional[bool] = False  # Optional field for fraud detection
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
