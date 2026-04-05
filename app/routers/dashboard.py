from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.record import FinancialRecord
from app.security import get_current_user

router = APIRouter(prefix="/dashboard")

@router.get("/total-income")
def get_total_income(user = Depends(get_current_user),db: Session = Depends(get_db)):

    income = db.query(func.sum(FinancialRecord.amount))
    
    if user["role"] == "viewer":
        income = income.filter(FinancialRecord.created_by == user["user_id"])
    
    income = income.filter(FinancialRecord.type == "income").scalar() or 0.0
    return {"total_income": income}


@router.get("/total-expense")
def get_total_expense(user = Depends(get_current_user),db: Session = Depends(get_db)):

    expense = db.query(func.sum(FinancialRecord.amount))
    
    if user["role"] == "viewer":
        expense = expense.filter(FinancialRecord.created_by == user["user_id"])

    expense = expense.filter(FinancialRecord.type == "expense").scalar() or 0.0
    return {"total_expense": expense}


@router.get("/net-balance")
def get_net_balance(user = Depends(get_current_user), db: Session = Depends(get_db)):

    income = db.query(func.sum(FinancialRecord.amount))
    expense = db.query(func.sum(FinancialRecord.amount))

    if user["role"] == "viewer":
        income = income.filter(FinancialRecord.created_by == user["user_id"])
        expense = expense.filter(FinancialRecord.created_by == user["user_id"])
    
    income = income.filter(FinancialRecord.type == "income").scalar() or 0.0
    expense = expense.filter(FinancialRecord.type == "expense").scalar() or 0.0
    net_balance = income - expense

    return {"net_balance": net_balance}


@router.get("/category-summary")
def get_category_summary(user = Depends(get_current_user),db : Session = Depends(get_db)):

    if user["role"] == "viewer":
        output = db.query(FinancialRecord.category, func.sum(FinancialRecord.amount)).filter(FinancialRecord.created_by == user["user_id"]).group_by(FinancialRecord.category)
    else:
        output = db.query(FinancialRecord.category, func.sum(FinancialRecord.amount)).group_by(FinancialRecord.category)

    return {category: total for category, total in output}



@router.get("/recent-records")
def get_recent_records(user = Depends(get_current_user), db: Session = Depends(get_db)):

    records = db.query(FinancialRecord)

    if user["role"] == "viewer":
        records = records.filter(FinancialRecord.created_by == user["user_id"])
    
    records = records.order_by(FinancialRecord.created_at.desc()).limit(5).all()
    return records


@router.get("/monthly-trends")
def get_trends(user= Depends(get_current_user), db: Session= Depends(get_db)):

    records = db.query(func.strftime("%Y-%m", FinancialRecord.date).label("month"), FinancialRecord.type, func.sum(FinancialRecord.amount).label("total"))

    if user["role"] == "viewer":
        records = records.filter(FinancialRecord.created_by == user["user_id"])

    records = records.group_by("month", FinancialRecord.type).all()

    trends = {}

    for month, _type, total in records:
        if month not in trends:
            trends[month] = {"income":0, "expense":0}
            
        trends[month][_type] = total
        
    return records