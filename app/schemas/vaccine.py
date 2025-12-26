"""
Vaccine Schemas - Data validation for vaccine records
"""

from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class VaccineBase(BaseModel):
    """Base Vaccine Schema"""
    vaccine_name: str = Field(..., min_length=1, max_length=100, description="Name of the vaccine")
    vaccine_type: Optional[str] = Field(None, max_length=50, description="Core, Non-core, Required")
    manufacturer: Optional[str] = Field(None, max_length=100)
    batch_number: Optional[str] = Field(None, max_length=50)
    date_given: date = Field(..., description="Date vaccine was administered")
    next_due_date: Optional[date] = Field(None, description="When booster is due")
    veterinarian_name: Optional[str] = Field(None, max_length=100)
    dosage: Optional[str] = Field(None, max_length=50)
    administration_route: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    adverse_reactions: Optional[str] = None


class VaccineCreate(VaccineBase):
    """Schema for creating a new vaccine record"""
    patient_id: int = Field(..., description="ID of the pet receiving the vaccine")


class VaccineUpdate(BaseModel):
    """Schema for updating a vaccine record"""
    vaccine_name: Optional[str] = Field(None, min_length=1, max_length=100)
    vaccine_type: Optional[str] = Field(None, max_length=50)
    manufacturer: Optional[str] = Field(None, max_length=100)
    batch_number: Optional[str] = Field(None, max_length=50)
    date_given: Optional[date] = None
    next_due_date: Optional[date] = None
    veterinarian_name: Optional[str] = Field(None, max_length=100)
    dosage: Optional[str] = Field(None, max_length=50)
    administration_route: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    adverse_reactions: Optional[str] = None


class Vaccine(VaccineBase):
    """Schema for returning vaccine data from API"""
    id: int
    patient_id: int
    tenant_id: int
    
    # Computed properties
    is_due_soon: bool
    is_overdue: bool
    days_until_due: Optional[int]
    
    model_config = ConfigDict(from_attributes=True)

