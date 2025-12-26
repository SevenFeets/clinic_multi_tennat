"""
Vaccine Model - Track vaccination history for pets

This model stores all vaccine records for each patient (pet).
Important for:
- Keeping vaccination schedules up to date
- Reminding owners of upcoming vaccines
- Compliance with veterinary regulations
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone, date, timedelta


class Vaccine(Base):
    """
    Vaccine Record Model
    
    Tracks each vaccination given to a pet.
    Includes next due date for booster shots.
    """
    __tablename__ = "vaccines"

    # Primary Key & Foreign Keys
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    # ==========================================
    # VACCINE INFORMATION
    # ==========================================
    vaccine_name = Column(String(100), nullable=False)  # "Rabies", "DHPP", "Bordetella"
    vaccine_type = Column(String(50), nullable=True)  # "Core", "Non-core", "Required by law"
    manufacturer = Column(String(100), nullable=True)  # Vaccine manufacturer
    batch_number = Column(String(50), nullable=True)  # Batch/lot number for tracking
    
    # ==========================================
    # DATES
    # ==========================================
    date_given = Column(Date, nullable=False, index=True)
    next_due_date = Column(Date, nullable=True, index=True)  # When booster is due
    
    # ==========================================
    # ADMINISTRATION DETAILS
    # ==========================================
    veterinarian_name = Column(String(100), nullable=True)  # Who administered
    dosage = Column(String(50), nullable=True)  # "1ml", "0.5ml"
    administration_route = Column(String(50), nullable=True)  # "Subcutaneous", "Intramuscular"
    
    # ==========================================
    # NOTES & REACTIONS
    # ==========================================
    notes = Column(Text, nullable=True)  # Any special notes
    adverse_reactions = Column(Text, nullable=True)  # Record any reactions
    
    # ==========================================
    # METADATA
    # ==========================================
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # ==========================================
    # RELATIONSHIPS
    # ==========================================
    patient = relationship("Patient", back_populates="vaccines")
    tenant = relationship("Tenant")
    
    # ==========================================
    # COMPUTED PROPERTIES
    # ==========================================
    @property
    def is_due_soon(self):
        """Check if vaccine is due within 30 days"""
        if self.next_due_date:
            today = date.today()
            days_until_due = (self.next_due_date - today).days
            return 0 <= days_until_due <= 30
        return False
    
    @property
    def is_overdue(self):
        """Check if vaccine is overdue"""
        if self.next_due_date:
            return date.today() > self.next_due_date
        return False
    
    @property
    def days_until_due(self):
        """Calculate days until next vaccine is due"""
        if self.next_due_date:
            return (self.next_due_date - date.today()).days
        return None
    
    def __repr__(self):
        return f"<Vaccine: {self.vaccine_name} for Patient #{self.patient_id} on {self.date_given}>"


# ==========================================
# COMMON VACCINES BY SPECIES
# ==========================================
"""
DOGS:
- Rabies (required by law in most places)
- DHPP (Distemper, Hepatitis, Parvovirus, Parainfluenza)
- Bordetella (Kennel Cough)
- Leptospirosis
- Lyme Disease
- Canine Influenza

CATS:
- Rabies (required by law)
- FVRCP (Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia)
- FeLV (Feline Leukemia)
- FIV (Feline Immunodeficiency Virus)

RABBITS:
- RHDV (Rabbit Hemorrhagic Disease Virus)
- Myxomatosis

BIRDS:
- Polyomavirus
- Pacheco's Disease
"""

