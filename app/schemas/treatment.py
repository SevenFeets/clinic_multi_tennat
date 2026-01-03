"""
Treatment Schemas - Data validation for treatment records
"""

from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TreatmentBase(BaseModel):
    """Base Treatment Schema"""
    treatment_type: str = Field(..., min_length=1, max_length=100, description="Type of treatment")
    treatment_name: str = Field(..., min_length=1, max_length=200, description="Name of treatment")
    treatment_date: date = Field(..., description="Date treatment was performed")
    follow_up_date: Optional[date] = Field(None, description="Follow-up appointment date")
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    treatment_plan: Optional[str] = None
    medications_prescribed: Optional[str] = None
    medication_instructions: Optional[str] = None
    veterinarian_name: Optional[str] = Field(None, max_length=100)
    cost: Optional[float] = Field(None, ge=0, description="Treatment cost")
    notes: Optional[str] = None
    outcome: Optional[str] = Field(None, max_length=50)


class TreatmentCreate(TreatmentBase):
    """Schema for creating a new treatment record"""
    patient_id: int = Field(..., description="ID of the pet receiving treatment")


class TreatmentUpdate(BaseModel):
    """Schema for updating a treatment record"""
    treatment_type: Optional[str] = Field(None, min_length=1, max_length=100)
    treatment_name: Optional[str] = Field(None, min_length=1, max_length=200)
    treatment_date: Optional[date] = None
    follow_up_date: Optional[date] = None
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    treatment_plan: Optional[str] = None
    medications_prescribed: Optional[str] = None
    medication_instructions: Optional[str] = None
    veterinarian_name: Optional[str] = Field(None, max_length=100)
    cost: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None
    outcome: Optional[str] = Field(None, max_length=50)


class Treatment(TreatmentBase):
    """Schema for returning treatment data from API"""
    id: int
    patient_id: int
    tenant_id: int
    
    model_config = ConfigDict(from_attributes=True)

