from pydantic import BaseModel, Field
from datetime import datetime, date
from enum import Enum

class RecordType(str, Enum):
    income = "income"
    expense = "expense"
    
class RecordCreate(BaseModel):
    amount: float = Field(gt=0, description="Amount must be greater than zero")
    type: RecordType
    category: str = Field(min_length=1, max_length=100, description="Category cannot be empty")
    date: date
    note:  str | None = Field(default=None, max_length=500)

class RecordResponse(BaseModel):
    id: int
    amount: float
    type: RecordType
    category: str
    date: date
    note : str | None
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
    