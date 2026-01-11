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
    
    # Calendar sync
    google_calendar_event_id = Column(String, nullable=True)  # Store Google Calendar event ID
    reminder_sent_at = Column(DateTime, nullable=True)  # Track when reminder was sent
    
    # Define relationships
    tenant = relationship("Tenant", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    
    def __repr__(self):
        return f"<Appointment {self.id} - Patient {self.patient_id} @ {self.appointment_time} ({self.status})>"


# Later:
# - Prevent double-booking (same time, same doctor)
# - Send reminders before appointments
# - Calculate no-show rates
# - Generate revenue reports
