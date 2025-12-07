from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    appointment_time = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, default=30)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled)
    notes = Column(Text)
    diagnosis = Column(Text)
    medicine_given = Column(Text)
    
    # Define relationships
    tenant = relationship("Tenant", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    
    def __repr__(self):
        return f"<Appointment {self.id} - Patient {self.patient_id} @ {self.appointment_time} ({self.status})>"


# Why use Enum for status?
# - Prevents typos ("schduled" vs "scheduled")
# - Database enforces valid values
# - Autocomplete in your IDE!
#
# Duration in minutes:
# - Easy to calculate end time
# - Easy to check for overlapping appointments
# - Standard: appointment_end = appointment_time + duration
#
# Notes vs Diagnosis:
# - notes: Things to remember (patient concerns, etc.)
# - diagnosis: Doctor's findings after appointment

# 💡 BUSINESS LOGIC IDEAS:
# Later, you'll want to:
# - Prevent double-booking (same time, same doctor)
# - Send reminders before appointments
# - Calculate no-show rates
# - Generate revenue reports

# 🧪 TESTING (Week 4):
# You'll create appointment booking endpoints
# Test edge cases: overlapping times, past dates, etc.

