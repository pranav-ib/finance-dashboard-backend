from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.record import FinancialRecord

router = APIRouter(prefix="/dashboard")

@router.get("/total-income")
def get_total_income(db: Session = Depends(get_db)):

    income = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == "income").scalar() or 0.0

    return {"total_income": income}

@router.get("/total-expense")
def get_total_expense(db: Session = Depends(get_db)):

    expense = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == "expense").scalar() or 0.0

    return {"total_expense": expense}

@router.get("/net-balance")
def get_net_balance(db: Session = Depends(get_db)):

    income = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == "income").scalar() or 0.0
    expense = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == "expense").scalar() or 0.0

    net_balance = income - expense

    return {"net_balance": net_balance}

@router.get("/category-summary")
def get_category_summary(db : Session = Depends(get_db)):

    output = db.query(FinancialRecord.category, func.sum(FinancialRecord.amount)).group_by(FinancialRecord.category)

    return {category: total for category, total in output}