from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name : str
    email: str
    password: str
    role: str = "viewer"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    status: str
    created_at:datetime

class LoginRequest(BaseModel):
    email: str
    password: str