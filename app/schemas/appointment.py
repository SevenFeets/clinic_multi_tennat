"""
Appointment Schemas - Pydantic models for appointment validation

🎯 YOUR MISSION (Week 4):
Create schemas for appointment booking and management

💡 HINTS:
- Validate appointment times are in the future
- Validate duration is reasonable
- Handle status enum properly
"""

# TODO: Import Pydantic
# HINT: from pydantic import BaseModel, validator
# HINT: from datetime import datetime
# HINT: from typing import Optional
# HINT: from app.models.appointment import AppointmentStatus


# TODO: Create AppointmentBase schema
# HINT: class AppointmentBase(BaseModel):
# HINT:     patient_id: int
# HINT:     appointment_time: datetime
# HINT:     duration_minutes: int = 30
# HINT:     notes: Optional[str] = None


# TODO: Create AppointmentCreate schema
# HINT: class AppointmentCreate(AppointmentBase):
# HINT:     pass
# HINT:     
# HINT:     # TODO: Add validator to ensure appointment is in the future
# HINT:     # @validator('appointment_time')
# HINT:     # def validate_future_time(cls, v):
# HINT:     #     if v < datetime.now():
# HINT:     #         raise ValueError("Appointment must be in the future")
# HINT:     #     return v


# TODO: Create AppointmentUpdate schema
# HINT: class AppointmentUpdate(BaseModel):
# HINT:     appointment_time: Optional[datetime] = None
# HINT:     duration_minutes: Optional[int] = None
# HINT:     status: Optional[AppointmentStatus] = None
# HINT:     notes: Optional[str] = None
# HINT:     diagnosis: Optional[str] = None


# TODO: Create Appointment schema (response)
# HINT: class Appointment(AppointmentBase):
# HINT:     id: int
# HINT:     tenant_id: int
# HINT:     status: AppointmentStatus
# HINT:     diagnosis: Optional[str] = None
# HINT:     
# HINT:     class Config:
# HINT:         from_attributes = True


# 📖 UNDERSTANDING:
# 
# DateTime validation:
# - Check appointment is in future
# - Check it's during business hours
# - Check for scheduling conflicts
#
# Business logic to add later:
# - Prevent appointments outside clinic hours
# - Check if time slot is available
# - Minimum notice period (e.g., 24 hours)

# 🎯 CHALLENGE:
# Add validators for:
# - duration_minutes (15, 30, 45, or 60 only)
# - appointment_time (must be on the hour or half-hour)
# - business hours (9 AM - 5 PM)

