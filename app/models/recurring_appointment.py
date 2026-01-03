"""
Recurring Appointment Model
For appointments that repeat on a schedule (daily, weekly, monthly, etc.)
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
import enum


class RecurrencePattern(str, enum.Enum):
    """How often the appointment repeats"""
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"


class RecurringAppointment(Base):
    __tablename__ = "recurring_appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    
    # Recurrence settings
    pattern = Column(Enum(RecurrencePattern), nullable=False)  # daily, weekly, monthly, yearly
    interval = Column(Integer, default=1)  # Every N days/weeks/months (e.g., every 2 weeks)
    
    # Start and end dates
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime, nullable=True)  # None = no end date
    time_of_day = Column(String, nullable=False)  # "09:00" format (HH:MM)
    duration_minutes = Column(Integer, default=30)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Additional info
    notes = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_generated = Column(DateTime)  # When we last created appointments from this template
    
    # Relationships
    tenant = relationship("Tenant", back_populates="recurring_appointments")
    patient = relationship("Patient", back_populates="recurring_appointments")
    
    def __repr__(self):
        return f"<RecurringAppointment {self.id} - Patient {self.patient_id} ({self.pattern})>"

