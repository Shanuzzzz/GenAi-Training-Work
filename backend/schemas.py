from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    caste_category: Optional[str] = None
    occupation: Optional[str] = None
    annual_income: Optional[int] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    age: Optional[int]
    gender: Optional[str]
    state: Optional[str]
    caste_category: Optional[str]
    occupation: Optional[str]
    annual_income: Optional[int]

    class Config:
        from_attributes = True

# --- Scheme Schemas ---
class SchemeBase(BaseModel):
    name: str
    description: str
    department: str
    state: str
    eligibility_criteria: dict
    benefits: str
    application_process: str
    documents_required: List[str]
    url: Optional[str] = None

class SchemeCreate(SchemeBase):
    pass

class SchemeResponse(SchemeBase):
    id: int

    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Chat & Agent Schemas ---
class ChatMessage(BaseModel):
    role: str
    content: str
    
class ChatQuery(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    suggested_actions: Optional[List[str]] = None
