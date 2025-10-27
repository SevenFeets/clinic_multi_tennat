"""
Appointment Model - Database table for appointments

🎯 YOUR MISSION (Week 4):
Create an Appointment model to track patient appointments

📚 LEARNING RESOURCES:
- DateTime in Python: https://realpython.com/python-datetime/
- Enum Types: For appointment status

💡 KEY CONCEPTS:
- Appointments link patients to time slots
- Track appointment status (scheduled, completed, cancelled)
- Belongs to tenant for multi-tenancy
"""

# TODO: Import SQLAlchemy components
# HINT: from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
# HINT: from sqlalchemy.orm import relationship
# HINT: import enum

# TODO: Import Base
# HINT: from app.database import Base


# TODO: Create an Enum for appointment status
# HINT: class AppointmentStatus(str, enum.Enum):
# HINT:     scheduled = "scheduled"
# HINT:     completed = "completed"
# HINT:     cancelled = "cancelled"
# HINT:     no_show = "no_show"


# TODO: Create Appointment class
# HINT: class Appointment(Base):

    # TODO: Set table name
    # HINT: __tablename__ = "appointments"
    
    # TODO: Define columns
    # HINT: id = Column(Integer, primary_key=True, index=True)
    # HINT: tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    # HINT: patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    # HINT: appointment_time = Column(DateTime, nullable=False)
    # HINT: duration_minutes = Column(Integer, default=30)
    # HINT: status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled)
    # HINT: notes = Column(Text)
    # HINT: diagnosis = Column(Text)
    
    # TODO: Define relationships
    # HINT: tenant = relationship("Tenant", back_populates="appointments")
    # HINT: patient = relationship("Patient", back_populates="appointments")


# 📖 UNDERSTANDING THE DESIGN:
# 
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

# 🎯 CHALLENGE:
# Add fields for:
# - doctor_id (ForeignKey to users who are doctors)
# - room_number (String)
# - appointment_type (enum: checkup, followup, emergency)
# - created_by (ForeignKey to user who created it)

# 💡 BUSINESS LOGIC IDEAS:
# Later, you'll want to:
# - Prevent double-booking (same time, same doctor)
# - Send reminders before appointments
# - Calculate no-show rates
# - Generate revenue reports

# 🧪 TESTING (Week 4):
# You'll create appointment booking endpoints
# Test edge cases: overlapping times, past dates, etc.

