"""
Waitlist Schemas - Data validation for waitlist operations
"""

from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime, timezone


class WaitlistBase(BaseModel):
    desired_date: datetime
    preferred_time_start: Optional[datetime] = None
    preferred_time_end: Optional[datetime] = None
    notes: Optional[str] = None
    contact_preference: Optional[str] = None
    priority: int = 0


class WaitlistCreate(WaitlistBase):
    patient_id: int
    
    @field_validator('desired_date')
    @classmethod
    def validate_future_date(cls, v: datetime) -> datetime:
        """Ensure desired date is in the future"""
        if v < datetime.now(timezone.utc):
            raise ValueError("Desired date must be in the future")
        return v
    
    @field_validator('contact_preference')
    @classmethod
    def validate_contact_preference(cls, v: Optional[str]) -> Optional[str]:
        """Validate contact preference"""
        if v and v not in ["email", "phone", "sms"]:
            raise ValueError("Contact preference must be 'email', 'phone', or 'sms'")
        return v
 

class WaitlistUpdate(BaseModel):
    desired_date: Optional[datetime] = None
    preferred_time_start: Optional[datetime] = None
    preferred_time_end: Optional[datetime] = None
    notes: Optional[str] = None
    contact_preference: Optional[str] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None


class Waitlist(WaitlistBase):
    id: int
    tenant_id: int
    patient_id: int
    is_active: bool
    created_at: datetime
    notified_at: Optional[datetime] = None
    fulfilled_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

