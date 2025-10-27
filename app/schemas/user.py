"""
User Schemas - Pydantic models for validation

🎯 YOUR MISSION (Week 2):
Create Pydantic schemas to validate user data

📚 LEARNING RESOURCES:
- Pydantic Tutorial: https://docs.pydantic.dev/latest/
- Data Validation: https://fastapi.tiangolo.com/tutorial/body/

💡 KEY CONCEPTS:
- SQLAlchemy Models = Database tables
- Pydantic Schemas = Data validation and serialization
- Schemas protect your API from bad data!
"""

# TODO: Import Pydantic components
# HINT: from pydantic import BaseModel, EmailStr, Field
# HINT: from datetime import datetime
# HINT: from typing import Optional


# TODO: Create UserBase schema (shared fields)
# HINT: class UserBase(BaseModel):
# HINT:     email: EmailStr  # Validates email format!
# HINT:     full_name: Optional[str] = None


# TODO: Create UserCreate schema (for registration)
# HINT: class UserCreate(UserBase):
# HINT:     password: str = Field(..., min_length=8)
# NOTE: This is what clients send when creating a user


# TODO: Create UserLogin schema (for login)
# HINT: class UserLogin(BaseModel):
# HINT:     email: EmailStr
# HINT:     password: str


# TODO: Create User schema (response model)
# HINT: class User(UserBase):
# HINT:     id: int
# HINT:     is_active: bool
# HINT:     created_at: datetime
# HINT:     tenant_id: Optional[int] = None
# HINT:     
# HINT:     class Config:
# HINT:         from_attributes = True  # Allows reading from SQLAlchemy models


# TODO: Create Token schema (for JWT responses)
# HINT: class Token(BaseModel):
# HINT:     access_token: str
# HINT:     token_type: str = "bearer"


# TODO: Create TokenData schema (decoded token)
# HINT: class TokenData(BaseModel):
# HINT:     email: Optional[str] = None


# 📖 UNDERSTANDING SCHEMAS:
# 
# Why separate Create and Response schemas?
# - UserCreate: Has password (client sends this)
# - User: No password! (API returns this)
# - NEVER return passwords to clients!
#
# What does EmailStr do?
# - Validates email format automatically
# - Rejects invalid emails like "notanemail"
# - Install email-validator package for this
#
# What's Optional[str]?
# - Field can be string or None
# - Makes the field not required
#
# Field() validation:
# - min_length=8: Password must be 8+ characters
# - ... means field is required

# 🎯 CHALLENGE:
# Add password strength validation:
# - At least one uppercase letter
# - At least one number
# HINT: Use @validator decorator from Pydantic

# 🧪 TESTING:
# from app.schemas.user import UserCreate
# user = UserCreate(email="test@example.com", password="weak")
# ^ This will fail because password is < 8 chars!

