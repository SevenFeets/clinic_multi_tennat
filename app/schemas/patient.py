from datetime import date
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional
import re

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: date = Field(..., description="Date of birth")
    address: Optional[str] = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        # Remove spaces and dashes
        phone = v.replace(' ', '').replace('-', '')
        # Check if it's a valid format
        if not re.match(r'^\d{10}$', phone):
            raise ValueError("Invalid phone number")
        return phone

class PatientCreate(PatientBase):
    medical_history: Optional[str] = None

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None

class Patient(PatientBase):
    id: int
    tenant_id: int
    medical_history: Optional[str] = None
    # Pydantic V2 config - allows reading from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

    
    
# Why PatientUpdate has all Optional fields?
# - Allows partial updates (update just email, or just phone)
# - Client sends only fields they want to change
# - Common pattern for PATCH endpoints


