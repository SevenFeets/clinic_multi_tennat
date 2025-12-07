from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

from datetime import datetime, timezone
from sqlalchemy import DateTime

class Patient(Base):

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # Define relationships
    tenant = relationship("Tenant", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    
    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name} (ID: {self.id})>"




# Why tenant_id in every model?
# - Ensures data isolation
# - Each tenant only sees their patients
# - Critical for privacy and security!
#
# Text vs String:
# - String: Short text (names, email) - limited length
# - Text: Long text (medical history) - unlimited length
#
# Date vs DateTime:
# - Date: Just the date (birthdate)
# - DateTime: Date and time (appointment time)

# ⚠️ IMPORTANT: Privacy & Security
# - Never log patient information
# - Always use HTTPS in production
# - Consider encryption for sensitive fields
# - Follow HIPAA guidelines if in the US

# 🧪 TESTING (Week 4):
# You'll create CRUD endpoints for patients

