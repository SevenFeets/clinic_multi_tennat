"""
Treatment Model - Track medical treatments for pets

This model stores all medical treatments, procedures, and visits
for each patient (pet).

Examples:
- Dental cleaning
- Surgery
- Medication prescribed
- Diagnostic tests
- Emergency visits
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime, Float
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone


class Treatment(Base):
    """
    Treatment Record Model
    
    Tracks all medical treatments, procedures, and visits.
    Includes diagnosis, treatment plan, and follow-up information.
    """
    __tablename__ = "treatments"

    # Primary Key & Foreign Keys
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    # ==========================================
    # TREATMENT INFORMATION
    # ==========================================
    treatment_type = Column(String(100), nullable=False, index=True)  # "Surgery", "Checkup", "Emergency"
    treatment_name = Column(String(200), nullable=False)  # "Dental Cleaning", "Spay Surgery"
    
    # ==========================================
    # DATES
    # ==========================================
    treatment_date = Column(Date, nullable=False, index=True)
    follow_up_date = Column(Date, nullable=True)  # When to return for follow-up
    
    # ==========================================
    # MEDICAL DETAILS
    # ==========================================
    diagnosis = Column(Text, nullable=True)  # What was diagnosed
    symptoms = Column(Text, nullable=True)  # Symptoms presented
    treatment_plan = Column(Text, nullable=True)  # What was done/prescribed
    
    # ==========================================
    # MEDICATIONS
    # ==========================================
    medications_prescribed = Column(Text, nullable=True)  # List of medications
    medication_instructions = Column(Text, nullable=True)  # How to administer
    
    # ==========================================
    # STAFF & COST
    # ==========================================
    veterinarian_name = Column(String(100), nullable=True)  # Who performed treatment
    cost = Column(Float, nullable=True)  # Treatment cost
    
    # ==========================================
    # NOTES & OUTCOMES
    # ==========================================
    notes = Column(Text, nullable=True)  # Additional notes
    outcome = Column(String(50), nullable=True)  # "Successful", "Ongoing", "Referred"
    
    # ==========================================
    # METADATA
    # ==========================================
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # ==========================================
    # RELATIONSHIPS
    # ==========================================
    patient = relationship("Patient", back_populates="treatments")
    tenant = relationship("Tenant")
    
    def __repr__(self):
        return f"<Treatment: {self.treatment_name} for Patient #{self.patient_id} on {self.treatment_date}>"


# ==========================================
# COMMON TREATMENT TYPES
# ==========================================
"""
PREVENTIVE:
- Annual checkup
- Dental cleaning
- Wellness exam
- Vaccination visit

SURGICAL:
- Spay/Neuter
- Dental surgery
- Tumor removal
- Orthopedic surgery
- Emergency surgery

DIAGNOSTIC:
- Blood work
- X-rays
- Ultrasound
- Biopsy
- Urinalysis

MEDICAL:
- Infection treatment
- Parasite treatment
- Chronic disease management
- Pain management
- Wound care

EMERGENCY:
- Trauma
- Poisoning
- Acute illness
- Foreign body removal
"""

