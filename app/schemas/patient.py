"""
Patient Schemas - Pydantic models for patient validation

🎯 YOUR MISSION (Week 4):
Create schemas for patient management

💡 HINTS:
- Follow the same pattern
- Validate phone numbers and emails
- Handle optional fields properly
"""

# TODO: Import Pydantic
# HINT: from pydantic import BaseModel, EmailStr
# HINT: from datetime import date
# HINT: from typing import Optional


# TODO: Create PatientBase schema
# HINT: class PatientBase(BaseModel):
# HINT:     first_name: str
# HINT:     last_name: str
# HINT:     email: Optional[EmailStr] = None
# HINT:     phone: Optional[str] = None
# HINT:     date_of_birth: Optional[date] = None
# HINT:     address: Optional[str] = None


# TODO: Create PatientCreate schema
# HINT: class PatientCreate(PatientBase):
# HINT:     medical_history: Optional[str] = None


# TODO: Create PatientUpdate schema
# HINT: class PatientUpdate(BaseModel):
# HINT:     # All fields optional for partial updates
# HINT:     first_name: Optional[str] = None
# HINT:     last_name: Optional[str] = None
# HINT:     email: Optional[EmailStr] = None
# HINT:     # ... add other fields as Optional


# TODO: Create Patient schema (response)
# HINT: class Patient(PatientBase):
# HINT:     id: int
# HINT:     tenant_id: int
# HINT:     
# HINT:     class Config:
# HINT:         from_attributes = True


# 📖 UNDERSTANDING:
# 
# Why PatientUpdate has all Optional fields?
# - Allows partial updates (update just email, or just phone)
# - Client sends only fields they want to change
# - Common pattern for PATCH endpoints

# 🎯 CHALLENGE:
# Add phone number validation using a @validator
# - Remove spaces and dashes
# - Check if it's a valid format

