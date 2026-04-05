from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.security import get_current_user

router = APIRouter(prefix="/user")


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db : Session= Depends(get_db)):
    
    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        name= user.name,
        email=user.email,
        password  = user.password,
        role = user.role 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=list[UserResponse])
def get_users(user=Depends(get_current_user), db:Session = Depends(get_db)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    users = db.query(User).all()

    return users

