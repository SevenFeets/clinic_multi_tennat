from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Float, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone, date
from sqlalchemy import DateTime
import enum

class GenderEnum(enum.Enum):
    """Gender options for pets"""
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"

class SpeciesEnum(enum.Enum):
    """Common pet species"""
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    HAMSTER = "hamster"
    GUINEA_PIG = "guinea_pig"
    REPTILE = "reptile"
    OTHER = "other"

class Patient(Base):
    """
    Patient Model - Represents a PET (not the owner)
    
    This is the core model for veterinary clinic management.
    Each patient is a pet (dog, cat, etc.) with owner information.
    """
    __tablename__ = "patients"

    # Primary Key & Tenant
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)

    # ==========================================
    # PET INFORMATION
    # ==========================================
    pet_name = Column(String(100), nullable=False, index=True)
    species = Column(String(50), nullable=False)  # "dog", "cat", "bird", etc.
    breed = Column(String(100), nullable=True)  # "Golden Retriever", "Persian Cat"
    color = Column(String(50), nullable=True)  # "Golden", "Black", "White"
    gender = Column(String(20), nullable=True)  # "male", "female", "unknown"
    date_of_birth = Column(Date, nullable=True)
    
    # Microchip Information
    chip_number = Column(String(20), unique=True, nullable=True, index=True)
    
    # Physical Characteristics
    weight = Column(Float, nullable=True)  # Weight in kg
    
    # ==========================================
    # OWNER INFORMATION
    # ==========================================
    owner_first_name = Column(String(100), nullable=False, index=True)
    owner_last_name = Column(String(100), nullable=False, index=True)
    owner_email = Column(String(255), nullable=True)
    owner_phone = Column(String(20), nullable=True, index=True)
    owner_address = Column(Text, nullable=True)
    
    # ==========================================
    # MEDICAL INFORMATION
    # ==========================================
    medical_history = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    special_notes = Column(Text, nullable=True)
    
    # ==========================================
    # METADATA
    # ==========================================
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    # ==========================================
    # RELATIONSHIPS
    # ==========================================
    tenant = relationship("Tenant", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    vaccines = relationship("Vaccine", back_populates="patient", cascade="all, delete-orphan")
    treatments = relationship("Treatment", back_populates="patient", cascade="all, delete-orphan")
    
    # ==========================================
    # COMPUTED PROPERTIES
    # ==========================================
    @property
    def age_years(self):
        """Calculate pet's age in years"""
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            # Adjust if birthday hasn't occurred this year
            if today.month < self.date_of_birth.month or \
               (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            return age
        return None
    
    @property
    def owner_full_name(self):
        """Get owner's full name"""
        return f"{self.owner_first_name} {self.owner_last_name}"
    
    @property
    def display_name(self):
        """Get pet display name with owner"""
        return f"{self.pet_name} ({self.owner_last_name})"
    
    def __repr__(self):
        return f"<Patient: {self.pet_name} ({self.species}) - Owner: {self.owner_full_name}>"




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

