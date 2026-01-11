"""
User Schemas - Pydantic models for validation
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Base schema with fields shared across user operations."""
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    tenant_id: int = Field(..., description="ID of the tenant/clinic this user belongs to")
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength requirements."""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v


class UserLogin(BaseModel):
    """Schema for user authentication."""
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    """Schema for returning user data."""
    id: int
    photo_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    is_superuser: bool = False
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    photo_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class PasswordChange(BaseModel):
    """Schema for changing user password."""
    old_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength requirements."""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """JWT token response after successful authentication."""
    access_token: str
    token_type: str = "bearer"
    user: Optional['User'] = None
    model_config = ConfigDict(from_attributes=True)


Token.model_rebuild()


class TokenData(BaseModel):
    """Data extracted from a decoded JWT token."""
    email: str
