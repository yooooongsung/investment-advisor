from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserSignup(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=2)
    age: int = Field(..., ge=18, le=100)
    investment_style: str
    investment_goal: str
    budget: int = Field(..., ge=0)
    experience: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    username: str
    name: str
    age: int
    investment_style: str
    investment_goal: str
    budget: int
    experience: str
    created_at: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile
