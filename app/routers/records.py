from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.record import FinancialRecord
from app.schemas.record_schema import RecordCreate, RecordResponse

router = APIRouter(prefix="/records")

@router.post("/")
def create_record(record: RecordCreate, db: Session = Depends(get_db)):

    new_record = FinancialRecord(
        amount = record.amount,
        type = record.type,
        category = record.category,
        date= record.date,
        note = record.note,
        created_by = 1
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record