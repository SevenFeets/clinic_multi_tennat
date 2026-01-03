"""
Waitlist Model - For managing appointment waitlist
When a desired time slot is unavailable, patients can join the waitlist.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Waitlist(Base):
    __tablename__ = "waitlist"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    
    # Desired appointment time
    desired_date = Column(DateTime, nullable=False, index=True)
    preferred_time_start = Column(DateTime)  # Optional: preferred start time
    preferred_time_end = Column(DateTime)    # Optional: preferred end time
    
    # Waitlist status
    is_active = Column(Boolean, default=True, index=True)  # True if still waiting
    priority = Column(Integer, default=0)  # Higher number = higher priority
    
    # Additional info
    notes = Column(Text)  # Why they need this appointment
    contact_preference = Column(String)  # "email", "phone", "sms"
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    notified_at = Column(DateTime)  # When we notified them of availability
    fulfilled_at = Column(DateTime)  # When appointment was created from waitlist
    
    # Relationships
    tenant = relationship("Tenant", back_populates="waitlist_entries")
    patient = relationship("Patient", back_populates="waitlist_entries")
    
    def __repr__(self):
        return f"<Waitlist {self.id} - Patient {self.patient_id} for {self.desired_date} (Active: {self.is_active})>"

