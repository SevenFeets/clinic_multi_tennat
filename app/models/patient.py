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

# TODO: Import SQLAlchemy components
# HINT: from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
# HINT: from sqlalchemy.orm import relationship

# TODO: Import Base
# HINT: from app.database import Base


# TODO: Create Patient class
# HINT: class Patient(Base):

    # TODO: Set table name
    # HINT: __tablename__ = "patients"
    
    # TODO: Define columns
    # HINT: id = Column(Integer, primary_key=True, index=True)
    # HINT: tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    # HINT: first_name = Column(String, nullable=False)
    # HINT: last_name = Column(String, nullable=False)
    # HINT: email = Column(String)
    # HINT: phone = Column(String)
    # HINT: date_of_birth = Column(Date)
    # HINT: address = Column(Text)
    # HINT: medical_history = Column(Text)  # Store medical notes
    
    # TODO: Define relationships
    # HINT: tenant = relationship("Tenant", back_populates="patients")
    # HINT: appointments = relationship("Appointment", back_populates="patient")


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

# 🎯 CHALLENGE:
# Add fields for:
# - insurance_provider (String)
# - insurance_number (String)
# - emergency_contact_name (String)
# - emergency_contact_phone (String)

# ⚠️ IMPORTANT: Privacy & Security
# - Never log patient information
# - Always use HTTPS in production
# - Consider encryption for sensitive fields
# - Follow HIPAA guidelines if in the US

# 🧪 TESTING (Week 4):
# You'll create CRUD endpoints for patients

