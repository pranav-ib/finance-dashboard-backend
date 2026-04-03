from fastapi import APIRouter, Depends, HTTPException
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

@router.put("/{record_id}")
def update_record(record_id: int, record: RecordCreate, db: Session = Depends(get_db)):

    exist_record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    if not exist_record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    exist_record.amount= record.amount
    exist_record.type = record.type
    exist_record.category = record.category
    exist_record.date = record.date
    exist_record.note= record.note

    db.commit()
    db.refresh(exist_record)

    return exist_record

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):

    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()

    return {"message": "Record Deleted"}
