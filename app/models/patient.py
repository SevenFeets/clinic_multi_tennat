"""
Patient Model - Database table for patients

🎯 YOUR MISSION (Week 4):
Create a Patient model with proper fields

📚 LEARNING RESOURCES:
- Data Privacy: HIPAA compliance basics (important for healthcare!)
- Database Relationships: One-to-many (one patient, many appointments)

💡 KEY CONCEPTS:
- Patients belong to a tenant (multi-tenancy)
- Patients can have many appointments
- Store patient medical information securely
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

from datetime import datetime, timezone

class Patient(Base):

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    medical_history = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    created_at = Column(datetime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(datetime, default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc))

    # Define relationships
    tenant = relationship("Tenant", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    

# 📖 UNDERSTANDING THE DESIGN:
# 
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

