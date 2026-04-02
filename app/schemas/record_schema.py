from pydantic import BaseModel
from datetime import datetime, date

class RecordCreate(BaseModel):
    amount: float
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
    