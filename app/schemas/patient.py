"""
Patient Schemas - Data validation for Pet records

These schemas define what data is required/optional when:
- Creating a new pet record
- Updating an existing pet
- Returning pet data from API
"""

from datetime import date
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional
import re


class PatientBase(BaseModel):
    """
    Base Patient Schema
    
    Contains fields common to all patient operations.
    Patient = PET (not owner)
    """
    # ==========================================
    # PET INFORMATION
    # ==========================================
    pet_name: str = Field(..., min_length=1, max_length=100, description="Pet's name")
    species: str = Field(..., description="dog, cat, bird, rabbit, etc.")
    breed: Optional[str] = Field(None, max_length=100, description="Breed of the pet")
    color: Optional[str] = Field(None, max_length=50, description="Pet's color")
    gender: Optional[str] = Field(None, description="male, female, or unknown")
    date_of_birth: Optional[date] = Field(None, description="Pet's date of birth")
    chip_number: Optional[str] = Field(None, max_length=20, description="Microchip number")
    weight: Optional[float] = Field(None, gt=0, description="Weight in kg")
    
    # ==========================================
    # OWNER INFORMATION
    # ==========================================
    owner_first_name: str = Field(..., min_length=1, max_length=100, description="Owner's first name")
    owner_last_name: str = Field(..., min_length=1, max_length=100, description="Owner's last name")
    owner_email: Optional[EmailStr] = Field(None, description="Owner's email")
    owner_phone: Optional[str] = Field(None, description="Owner's phone number")
    owner_address: Optional[str] = Field(None, description="Owner's address")
    
    # ==========================================
    # VALIDATORS
    # ==========================================
    @field_validator('owner_phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate and format phone number"""
        if v is None:
            return None
        # Remove spaces, dashes, and parentheses
        phone = v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        # Check if it's a valid format (10-15 digits)
        if not re.match(r'^\d{10,15}$', phone):
            raise ValueError("Phone number must be 10-15 digits")
        return phone
    
    @field_validator('species')
    @classmethod
    def validate_species(cls, v: str) -> str:
        """Validate and normalize species"""
        valid_species = ['dog', 'cat', 'bird', 'rabbit', 'hamster', 'guinea_pig', 'reptile', 'other']
        v_lower = v.lower()
        if v_lower not in valid_species:
            # Allow it but warn in logs
            pass
        return v_lower
    
    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v: Optional[str]) -> Optional[str]:
        """Validate and normalize gender"""
        if v is None:
            return None
        valid_genders = ['male', 'female', 'unknown']
        v_lower = v.lower()
        if v_lower not in valid_genders:
            return 'unknown'
        return v_lower
    
    @field_validator('chip_number')
    @classmethod
    def validate_chip_number(cls, v: Optional[str]) -> Optional[str]:
        """Validate microchip number format"""
        if v is None:
            return None
        # Remove spaces and dashes
        chip = v.replace(' ', '').replace('-', '')
        # Microchips are typically 9-15 digits
        if not re.match(r'^\d{9,15}$', chip):
            raise ValueError("Chip number must be 9-15 digits")
        return chip


class PatientCreate(PatientBase):
    """
    Schema for creating a new patient (pet)
    
    Includes optional medical information fields.
    """
    medical_history: Optional[str] = Field(None, description="Medical history notes")
    allergies: Optional[str] = Field(None, description="Known allergies")
    special_notes: Optional[str] = Field(None, description="Special care instructions")


class PatientUpdate(BaseModel):
    """
    Schema for updating an existing patient
    
    All fields are optional - only send what you want to update.
    This is for PATCH operations (partial updates).
    """
    # Pet Information
    pet_name: Optional[str] = Field(None, min_length=1, max_length=100)
    species: Optional[str] = None
    breed: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    chip_number: Optional[str] = Field(None, max_length=20)
    weight: Optional[float] = Field(None, gt=0)
    
    # Owner Information
    owner_first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    owner_last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    owner_email: Optional[EmailStr] = None
    owner_phone: Optional[str] = None
    owner_address: Optional[str] = None
    
    # Medical Information
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    special_notes: Optional[str] = None


class Patient(PatientBase):
    """
    Schema for returning patient data from API
    
    Includes all fields from database, including computed properties.
    """
    id: int
    tenant_id: int
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    special_notes: Optional[str] = None
    
    # Computed properties (from model)
    age_years: Optional[int] = None
    owner_full_name: str
    display_name: str
    
    # Pydantic V2 config - allows reading from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

    
    
# Why PatientUpdate has all Optional fields?
# - Allows partial updates (update just email, or just phone)
# - Client sends only fields they want to change
# - Common pattern for PATCH endpoints


