"""
Recurring Appointment Schemas
"""

from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime, timezone
from app.models.recurring_appointment import RecurrencePattern


class RecurringAppointmentBase(BaseModel):
    pattern: RecurrencePattern
    interval: int = 1
    start_date: datetime
    end_date: Optional[datetime] = None
    time_of_day: str  # "09:00" format
    duration_minutes: int = 30
    notes: Optional[str] = None


class RecurringAppointmentCreate(RecurringAppointmentBase):
    patient_id: int
    
    @field_validator('time_of_day')
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        """Validate time format is HH:MM"""
        try:
            hour, minute = v.split(':')
            hour_int = int(hour)
            minute_int = int(minute)
            if not (0 <= hour_int < 24 and 0 <= minute_int < 60):
                raise ValueError("Invalid time")
            return v
        except (ValueError, AttributeError):
            raise ValueError("Time must be in HH:MM format (e.g., '09:00')")
    
    @field_validator('interval')
    @classmethod
    def validate_interval(cls, v: int) -> int:
        """Interval must be positive"""
        if v < 1:
            raise ValueError("Interval must be at least 1")
        return v
    
    @field_validator('start_date')
    @classmethod
    def validate_start_date(cls, v: datetime) -> datetime:
        """Start date should be in the future"""
        if v < datetime.now(timezone.utc):
            raise ValueError("Start date must be in the future")
        return v


class RecurringAppointmentUpdate(BaseModel):
    pattern: Optional[RecurrencePattern] = None
    interval: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    time_of_day: Optional[str] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class RecurringAppointment(RecurringAppointmentBase):
    id: int
    tenant_id: int
    patient_id: int
    is_active: bool
    created_at: datetime
    last_generated: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

