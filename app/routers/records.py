from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.record import FinancialRecord
from app.schemas.record_schema import RecordCreate, RecordResponse
from app.security import get_current_user

router = APIRouter(prefix="/records")

@router.post("/")
def create_record(record: RecordCreate,user = Depends(get_current_user), db: Session = Depends(get_db)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    new_record = FinancialRecord(
        amount = record.amount,
        type = record.type,
        category = record.category,
        date= record.date,
        note = record.note,
        created_by = user["user_id"]
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record

@router.put("/{record_id}")
def update_record(record_id: int, record: RecordCreate, user= Depends(get_current_user), db: Session = Depends(get_db)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
     
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
def delete_record(record_id: int,user=Depends(get_current_user), db: Session = Depends(get_db)):

    if user["role"] != "admin":
       raise HTTPException(status_code=403, detail="Access denied")
     
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(record)
    db.commit()

    return {"message": "Record Deleted"}

@router.get("/", response_model=list[RecordResponse])
def get_records(
    type: str | None = Query(None),
    category: str | None = Query(None),
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    user=Depends(get_current_user),
    db : Session = Depends(get_db)):

    records = db.query(FinancialRecord)

    if user["role"] == "viewer":
        records = records.filter(FinancialRecord.created_by == user["user_id"])
            
    if type:
        records = records.filter(FinancialRecord.type == type)

    if category:
        records = records.filter(FinancialRecord.category == category)

    if start_date:
        records = records.filter(FinancialRecord.date >= start_date)
    
    if end_date:
        records = records.filter(FinancialRecord.date <= end_date)

    return records.all()