from pydantic import BaseModel, Field
from datetime import datetime, date

class RecordCreate(BaseModel):
    amount: float = Field(gt=0)
    type: str
    category: str
    date: date
    note:  str | None

class RecordResponse(BaseModel):
    id: int
    amount: float
    type:str
    category: str
    date: date
    note : str | None
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
    