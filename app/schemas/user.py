"""
User Schemas - Pydantic models for validation

YOUR MISSION (Week 2):
Create Pydantic schemas to validate user data

 KEY CONCEPTS:
- SQLAlchemy Models = Database tables
- Pydantic Schemas = Data validation and serialization
- Schemas protect your API from bad data!
"""

# Import Pydantic components
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

# UserBase: Shared fields used by multiple schemas
class UserBase(BaseModel):
    """
    Base schema with fields shared across user operations.
    This gets inherited by UserCreate and User schemas.
    """
    email: EmailStr  # Automatically validates email format! (needs email-validator package)
    full_name: str  # Required field - must match database constraint (nullable=False)


# UserCreate: What clients send when registering
class UserCreate(UserBase):
    """
    Schema for user registration.
    Inherits email and full_name from UserBase.
    Adds password field with validation.
    
    Example:
    {
        "email": "john@example.com",
        "full_name": "John Doe",
        "password": "SecurePass123",
        "tenant_id": 1
    }
    """
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    tenant_id: int = Field(..., description="ID of the tenant/clinic this user belongs to")
    
    # Password strength validation
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password strength requirements:
        - At least 8 characters (enforced by Field min_length)
        - At least one number
        - At least one uppercase letter
        - At least one lowercase letter
        """
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v
    
    # 🔒 SECURITY NOTE: This schema is ONLY for input. 
    # We NEVER return this from our API (would expose passwords!)


# UserLogin: What clients send when logging in
class UserLogin(BaseModel):
    """
    Schema for user authentication.
    Simple: just email and password.
    
    Example:
    {
        "email": "john@example.com",
        "password": "SecurePass123"
    }
    """
    email: EmailStr
    password: str  # No min_length here - we're checking if it exists, not creating new
    model_config = ConfigDict(from_attributes=True)

# User: What we return to clients (response model)
class User(UserBase):
    """
    Schema for returning user data.
    Inherits email and full_name from UserBase.
    Adds database fields like id, created_at.
    
    🔒 CRITICAL: NO PASSWORD FIELD! Never return passwords!
    
    Example Response:
    {
        "id": 1,
        "email": "john@example.com",
        "full_name": "John Doe",
        "is_active": true,
        "created_at": "2025-11-04T10:30:00",
        "tenant_id": null
    }
    """
    id: int
    is_active: bool
    created_at: datetime
    is_superuser: bool = False
    # tenant_id: Optional[int] = None  # Commented out until we create Tenant model
    
    # Pydantic V2 config - allows reading from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


# Token: What we return after successful login
class Token(BaseModel):
    """
    JWT token response after successful authentication.
    
    Example Response after login:
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "user": { ... }  # Optional user object
    }
    """
    access_token: str  # The actual JWT token
    token_type: str = "bearer"  # Standard OAuth2 token type
    user: Optional['User'] = None  # Include user info in login response
    
    model_config = ConfigDict(from_attributes=True)


# Rebuild Token model to resolve forward references
# This is required in Pydantic v2 when using forward references like Optional['User']
Token.model_rebuild()


# TokenData: What's inside the token (decoded)
class TokenData(BaseModel):
    """
    Data extracted from a decoded JWT token.
    Used internally to identify the user from their token.
    
    Note: If token is invalid or missing required fields, verify_token() 
    returns None rather than a TokenData with None fields.
    """
    email: str  # User's email from token payload (always present in valid tokens)


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
# HINT: Use @field_validator v2 decorator from Pydantic

# 🧪 TESTING:
# from app.schemas.user import UserCreate
# user = UserCreate(email="test@example.com", password="weak")
# ^ This will fail because password is < 8 chars!

