""" MISSION (Week 4):
Create RESTful endpoints for patient management

📚 LEARNING RESOURCES:
- REST API Design: https://restfulapi.net/
- CRUD Operations: https://www.codecademy.com/article/what-is-crud
- FastAPI Path Parameters: https://fastapi.tiangolo.com/tutorial/path-params/
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
# modules
from app.database import get_db
from app.models.patient import Patient
from app.schemas.patient import Patient as PatientSchema, PatientCreate, PatientUpdate
from app.auth.dependencies import get_current_active_user
from app.models.user import User
from sqlalchemy import or_


# create router
router = APIRouter(prefix='/patients', tags=['Patients'])

@router.post("/", response_model=PatientSchema, status_code=status.HTTP_201_CREATED)
async def create_patient(
        patient_data: PatientCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):

# Create new patient

            # The ** operator is "dictionary unpacking" in Python.
            # It converts all key-value pairs from patient_data.dict() into keyword arguments
            # for the Patient constructor. For example, if patient_data.dict() is {"name": "Alice", "dob": "2000-01-01"}
            # then Patient(**patient_data.dict(), tenant_id=current_user.tenant_id) is equivalent to:
            #   Patient(name="Alice", dob="2000-01-01", tenant_id=current_user.tenant_id)
            new_patient = Patient(**patient_data.model_dump(), tenant_id=current_user.tenant_id)
            db.add(new_patient)
            db.commit()
            db.refresh(new_patient)

            return new_patient


# ⚠️ IMPORTANT: Search routes MUST come BEFORE /{patient_id} route!
# Otherwise FastAPI thinks "search" is a patient_id

# Search all fields endpoint
@router.get("/search", response_model=List[PatientSchema])
async def search_patients(
    search_query: str,
    db: Session= Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Search patients across all text fields.
    Case-insensitive search using ILIKE.
    """
    # or must be in brackets
    patients = db.query(Patient).filter(
        Patient.tenant_id == current_user.tenant_id, 
        or_(
        Patient.first_name.ilike(f"%{search_query}%"),
        Patient.last_name.ilike(f"%{search_query}%"),
        Patient.email.ilike(f"%{search_query}%"),
        Patient.phone.ilike(f"%{search_query}%"),
        Patient.address.ilike(f"%{search_query}%"),
        Patient.medical_history.ilike(f"%{search_query}%"), 
        )
    ).all()
    return patients


# Search patients by name endpoint
@router.get("/search/by_name", response_model=List[PatientSchema])
async def search_patients_by_name(
    search_query: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Search patients by first or last name only.
    More specific than general search.
    """
    patients = db.query(Patient).filter(
        Patient.tenant_id == current_user.tenant_id,
        or_(
        Patient.first_name.ilike(f"%{search_query}%"),
        Patient.last_name.ilike(f"%{search_query}%"),
        )
    ).all()
    return patients


# Get all patients endpoint (with pagination)
@router.get("/", response_model=List[PatientSchema])
async def get_patients(
    skip: int = 0, # means skip the first 0 patients
    limit: int = 100, # limit the number of patients returned
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all patients for the current tenant with pagination.
    Only returns patients from current user's tenant (security).
    """
    # This line queries the database for all Patient records that belong to the current user's tenant.
    # - db.query(Patient): starts a query for Patient objects.
    # - .filter(Patient.tenant_id == current_user.tenant_id): ensures only patients from the same tenant (clinic) as the user are selected (important for security and multi-tenancy).
    # - .offset(skip).limit(limit): pagination to skip a number of records and limit how many are returned.
    # - .all(): executes the query and returns a list of Patient objects.
    patients = db.query(Patient).filter(
        Patient.tenant_id == current_user.tenant_id
    ).offset(skip).limit(limit).all()
    
    return patients


# Get patient by id endpoint
@router.get("/{patient_id}", response_model=PatientSchema)
async def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):

   
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        # security check!
        Patient.tenant_id == current_user.tenant_id
    ).first()


    # if patient not found, raise 404 error
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    return patient


# update endpoint
@router.patch("/{patient_id}", response_model=PatientSchema)
async def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):

    # get patient (with tenant check)
    updated_patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.tenant_id == current_user.tenant_id,
        
    ).first()


    if not updated_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

   
    # update only provided fields
    # patient_data.dict(exclude_unset=True) creates a dictionary containing ONLY the fields
    # that were explicitly provided in the request. This means if someone only wants to update
    # the phone number, we won't accidentally set other fields to None.
    update_data = patient_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(updated_patient, field, value)

    db.commit()
    db.refresh(updated_patient)
    return updated_patient


# Delete patient endpoint
@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a patient from the system.
    Only works if patient belongs to current user's tenant.
    """
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.tenant_id == current_user.tenant_id
    ).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    db.delete(patient)
    db.commit()
    return None # 204 No Content



# TODO additional endpoints:

# - Get patient's appointment history
# - Upload patient documents
# - Export patient data (GDPR compliance)







# 📖 UNDERSTANDING CRUD:
# 
# REST Conventions:
# - POST /patients → Create new patient
# - GET /patients → List all patients
# - GET /patients/123 → Get patient #123
# - PATCH /patients/123 → Update patient #123
# - DELETE /patients/123 → Delete patient #123
#
# Multi-Tenancy Security:
# ALWAYS filter by tenant_id!
# Without this, users could access other tenants' data!
#
# Pagination:
# - skip: How many records to skip
# - limit: How many records to return
# - Example: skip=10, limit=10 → records 11-20



# ⚠️ SECURITY:
# - Always check tenant_id!
# - Validate user permissions (can they edit patients?)
# - Log access to medical records (audit trail)
# - Consider soft deletes instead of hard deletes

# 🧪 TESTING:
# 1. Create a patient
# 2. List patients (should see your patient)
# 3. Update patient info
# 4. Try to access with wrong patient_id → 404
# 5. Delete patient

# 💡 TIP:
# Test multi-tenancy:
# 1. Create two users in different tenants
# 2. Create patients for each
# 3. Verify each user only sees their patients!

