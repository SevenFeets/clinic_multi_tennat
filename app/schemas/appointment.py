from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime, timezone
from app.models.appointment import AppointmentStatus

class AppointmentBase(BaseModel):
    patient_id: int
    appointment_time: datetime
    duration_minutes: int = 30
    
    # other fiels may be added later

class AppointmentCreate(AppointmentBase):
    notes: Optional[str] = None
    diagnosis: Optional[str] = None
    medicine_given: Optional[str] = None

    @field_validator('appointment_time')
    @classmethod
    def validate_future_time(cls, v: datetime) -> datetime:
        if v < datetime.now(timezone.utc):
            raise ValueError("Appointment must be in the future")
        return v

    # optionall add validator for duration_minutes

class AppointmentUpdate(BaseModel):
    appointment_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None
    diagnosis: Optional[str] = None
    medicine_given: Optional[str] = None


class Appointment(AppointmentBase):
    id: int
    tenant_id: int
    status: AppointmentStatus
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    medicine_given: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

  
  
 


# DateTime validation:
# - Check appointment is in future
# - Check it's during business hours
# - Check for scheduling conflicts
#
# Business logic to add later:
# - Prevent appointments outside clinic hours
# - Check if time slot is available
# - Minimum notice period (e.g., 24 hours)

