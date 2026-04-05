from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.security import create_access_token, get_current_user, hash_password, verify_password
from app.schemas.user_schema import LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth")

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id, "role": user.role})

    return {"access_token": token}

@router.post("/register")
def register(user: RegisterRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        name= user.name,
        email=user.email,
        password  = hash_password(user.password),
        role = "viewer"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }