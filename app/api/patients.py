"""
Patient Endpoints - CRUD operations for patients

🎯 YOUR MISSION (Week 4):
Create RESTful endpoints for patient management

📚 LEARNING RESOURCES:
- REST API Design: https://restfulapi.net/
- CRUD Operations: https://www.codecademy.com/article/what-is-crud
- FastAPI Path Parameters: https://fastapi.tiangolo.com/tutorial/path-params/

💡 KEY CONCEPTS:
- CRUD = Create, Read, Update, Delete
- REST conventions: POST (create), GET (read), PUT/PATCH (update), DELETE (delete)
- Path parameters: /patients/{patient_id}
- Query parameters: /patients?skip=0&limit=10
"""

# TODO: Import FastAPI components
# HINT: from fastapi import APIRouter, Depends, HTTPException, status
# HINT: from sqlalchemy.orm import Session
# HINT: from typing import List

# TODO: Import your modules
# HINT: from app.database import get_db
# HINT: from app.models.patient import Patient
# HINT: from app.models.user import User
# HINT: from app.schemas.patient import Patient as PatientSchema, PatientCreate, PatientUpdate
# HINT: from app.auth.dependencies import get_current_active_user


# TODO: Create router
# HINT: router = APIRouter(prefix="/patients", tags=["Patients"])


# TODO: Create patient endpoint
# HINT: @router.post("/", response_model=PatientSchema, status_code=status.HTTP_201_CREATED)
# HINT: async def create_patient(
# HINT:     patient_data: PatientCreate,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     # Create new patient
# HINT:     new_patient = Patient(
# HINT:         **patient_data.dict(),
# HINT:         tenant_id=current_user.tenant_id  # Multi-tenancy!
# HINT:     )
# HINT:     
# HINT:     db.add(new_patient)
# HINT:     db.commit()
# HINT:     db.refresh(new_patient)
# HINT:     
# HINT:     return new_patient


# TODO: Get all patients endpoint (with pagination)
# HINT: @router.get("/", response_model=List[PatientSchema])
# HINT: async def get_patients(
# HINT:     skip: int = 0,
# HINT:     limit: int = 100,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     # Only get patients from current user's tenant!
# HINT:     patients = db.query(Patient).filter(
# HINT:         Patient.tenant_id == current_user.tenant_id
# HINT:     ).offset(skip).limit(limit).all()
# HINT:     
# HINT:     return patients


# TODO: Get single patient endpoint
# HINT: @router.get("/{patient_id}", response_model=PatientSchema)
# HINT: async def get_patient(
# HINT:     patient_id: int,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     patient = db.query(Patient).filter(
# HINT:         Patient.id == patient_id,
# HINT:         Patient.tenant_id == current_user.tenant_id  # Security check!
# HINT:     ).first()
# HINT:     
# HINT:     if not patient:
# HINT:         raise HTTPException(
# HINT:             status_code=status.HTTP_404_NOT_FOUND,
# HINT:             detail="Patient not found"
# HINT:         )
# HINT:     
# HINT:     return patient


# TODO: Update patient endpoint
# HINT: @router.patch("/{patient_id}", response_model=PatientSchema)
# HINT: async def update_patient(
# HINT:     patient_id: int,
# HINT:     patient_data: PatientUpdate,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     # Get patient (with tenant check)
# HINT:     patient = db.query(Patient).filter(
# HINT:         Patient.id == patient_id,
# HINT:         Patient.tenant_id == current_user.tenant_id
# HINT:     ).first()
# HINT:     
# HINT:     if not patient:
# HINT:         raise HTTPException(status_code=404, detail="Patient not found")
# HINT:     
# HINT:     # Update only provided fields
# HINT:     update_data = patient_data.dict(exclude_unset=True)
# HINT:     for field, value in update_data.items():
# HINT:         setattr(patient, field, value)
# HINT:     
# HINT:     db.commit()
# HINT:     db.refresh(patient)
# HINT:     
# HINT:     return patient


# TODO: Delete patient endpoint
# HINT: @router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
# HINT: async def delete_patient(
# HINT:     patient_id: int,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     patient = db.query(Patient).filter(
# HINT:         Patient.id == patient_id,
# HINT:         Patient.tenant_id == current_user.tenant_id
# HINT:     ).first()
# HINT:     
# HINT:     if not patient:
# HINT:         raise HTTPException(status_code=404, detail="Patient not found")
# HINT:     
# HINT:     db.delete(patient)
# HINT:     db.commit()
# HINT:     
# HINT:     return None  # 204 No Content


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

# 🎯 CHALLENGE:
# Add endpoints for:
# - Search patients by name
# - Get patient's appointment history
# - Upload patient documents
# - Export patient data (GDPR compliance)

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

