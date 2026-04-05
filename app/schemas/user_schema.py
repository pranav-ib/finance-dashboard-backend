from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"   
    analyst = "analyst"
    viewer = "viewer"

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    
class UserCreate(BaseModel):
    name : str = Field(min_length=1, max_length=100, description="Name cannot be empty")
    email: EmailStr
    password: str
    role: UserRole = UserRole.viewer

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    status: str
    created_at:datetime

    class Config:
      from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    name : str = Field(min_length=1, max_length=100, description="Name cannot be empty")
    email: EmailStr
    password: str = Field(min_length=6, description="Password must be at least 6 characters long")