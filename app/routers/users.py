from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/user")


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db : Session= Depends(get_db)):
    
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
def get_users(db:Session = Depends(get_db)):

    users = db.query(User).all()

    return users