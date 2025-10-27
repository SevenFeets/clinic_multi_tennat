"""
Appointment Endpoints - Book and manage appointments

🎯 YOUR MISSION (Week 4):
Create endpoints for appointment management with business logic

📚 LEARNING RESOURCES:
- DateTime in Python: https://realpython.com/python-datetime/
- Query Filtering: https://docs.sqlalchemy.org/en/20/orm/queryguide.html

💡 KEY CONCEPTS:
- Validate appointment times (no double booking!)
- Check business hours
- Verify patient belongs to same tenant
- Filter by date range
"""

# TODO: Import FastAPI components
# HINT: from fastapi import APIRouter, Depends, HTTPException, status, Query
# HINT: from sqlalchemy.orm import Session
# HINT: from typing import List, Optional
# HINT: from datetime import datetime, date

# TODO: Import your modules
# HINT: from app.database import get_db
# HINT: from app.models.appointment import Appointment, AppointmentStatus
# HINT: from app.models.patient import Patient
# HINT: from app.models.user import User
# HINT: from app.schemas.appointment import (
# HINT:     Appointment as AppointmentSchema,
# HINT:     AppointmentCreate,
# HINT:     AppointmentUpdate
# HINT: )
# HINT: from app.auth.dependencies import get_current_active_user


# TODO: Create router
# HINT: router = APIRouter(prefix="/appointments", tags=["Appointments"])


# TODO: Create appointment endpoint
# HINT: @router.post("/", response_model=AppointmentSchema, status_code=status.HTTP_201_CREATED)
# HINT: async def create_appointment(
# HINT:     appointment_data: AppointmentCreate,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     # Verify patient belongs to same tenant
# HINT:     patient = db.query(Patient).filter(
# HINT:         Patient.id == appointment_data.patient_id,
# HINT:         Patient.tenant_id == current_user.tenant_id
# HINT:     ).first()
# HINT:     
# HINT:     if not patient:
# HINT:         raise HTTPException(status_code=404, detail="Patient not found")
# HINT:     
# HINT:     # TODO: Add business logic
# HINT:     # - Check for time conflicts
# HINT:     # - Validate business hours
# HINT:     # - Check if time is in the future
# HINT:     
# HINT:     # Create appointment
# HINT:     new_appointment = Appointment(
# HINT:         **appointment_data.dict(),
# HINT:         tenant_id=current_user.tenant_id
# HINT:     )
# HINT:     
# HINT:     db.add(new_appointment)
# HINT:     db.commit()
# HINT:     db.refresh(new_appointment)
# HINT:     
# HINT:     return new_appointment


# TODO: Get appointments endpoint (with filters)
# HINT: @router.get("/", response_model=List[AppointmentSchema])
# HINT: async def get_appointments(
# HINT:     skip: int = 0,
# HINT:     limit: int = 100,
# HINT:     patient_id: Optional[int] = None,
# HINT:     status: Optional[AppointmentStatus] = None,
# HINT:     date_from: Optional[date] = None,
# HINT:     date_to: Optional[date] = None,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     # Base query with tenant filter
# HINT:     query = db.query(Appointment).filter(
# HINT:         Appointment.tenant_id == current_user.tenant_id
# HINT:     )
# HINT:     
# HINT:     # Apply optional filters
# HINT:     if patient_id:
# HINT:         query = query.filter(Appointment.patient_id == patient_id)
# HINT:     if status:
# HINT:         query = query.filter(Appointment.status == status)
# HINT:     if date_from:
# HINT:         query = query.filter(Appointment.appointment_time >= date_from)
# HINT:     if date_to:
# HINT:         query = query.filter(Appointment.appointment_time <= date_to)
# HINT:     
# HINT:     # Execute query with pagination
# HINT:     appointments = query.offset(skip).limit(limit).all()
# HINT:     
# HINT:     return appointments


# TODO: Get single appointment endpoint
# HINT: @router.get("/{appointment_id}", response_model=AppointmentSchema)
# HINT: async def get_appointment(
# HINT:     appointment_id: int,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     appointment = db.query(Appointment).filter(
# HINT:         Appointment.id == appointment_id,
# HINT:         Appointment.tenant_id == current_user.tenant_id
# HINT:     ).first()
# HINT:     
# HINT:     if not appointment:
# HINT:         raise HTTPException(status_code=404, detail="Appointment not found")
# HINT:     
# HINT:     return appointment


# TODO: Update appointment endpoint
# HINT: @router.patch("/{appointment_id}", response_model=AppointmentSchema)
# HINT: async def update_appointment(
# HINT:     appointment_id: int,
# HINT:     appointment_data: AppointmentUpdate,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     # Similar to patient update
# HINT:     # Get appointment, update fields, commit
# HINT:     pass  # TODO: Implement this!


# TODO: Cancel appointment endpoint
# HINT: @router.post("/{appointment_id}/cancel", response_model=AppointmentSchema)
# HINT: async def cancel_appointment(
# HINT:     appointment_id: int,
# HINT:     db: Session = Depends(get_db),
# HINT:     current_user: User = Depends(get_current_active_user)
# HINT: ):
# HINT:     appointment = db.query(Appointment).filter(
# HINT:         Appointment.id == appointment_id,
# HINT:         Appointment.tenant_id == current_user.tenant_id
# HINT:     ).first()
# HINT:     
# HINT:     if not appointment:
# HINT:         raise HTTPException(status_code=404, detail="Appointment not found")
# HINT:     
# HINT:     appointment.status = AppointmentStatus.cancelled
# HINT:     db.commit()
# HINT:     db.refresh(appointment)
# HINT:     
# HINT:     return appointment


# 📖 UNDERSTANDING APPOINTMENT LOGIC:
# 
# Business Rules to Implement:
# 1. No double booking (check for overlaps)
# 2. Business hours only (e.g., 9 AM - 5 PM)
# 3. Future dates only (can't book in the past)
# 4. Minimum notice period (e.g., 24 hours ahead)
# 5. Maximum booking range (e.g., 90 days ahead)
#
# Checking for Conflicts:
# New appointment: 10:00 AM - 10:30 AM
# Existing: 9:45 AM - 10:15 AM
# These overlap! Need to reject.
#
# Query for overlaps:
# - New start < Existing end AND
# - New end > Existing start

# 🎯 CHALLENGE:
# Implement:
# - check_time_conflict() function
# - Get available time slots for a date
# - Send appointment reminders
# - Calculate appointment statistics

# ⚠️ IMPORTANT:
# - Use timezone-aware datetimes
# - Handle daylight saving time
# - Consider different time zones (future)
# - Add proper indexes on appointment_time

# 🧪 TESTING:
# 1. Book an appointment
# 2. Try booking at same time → should fail
# 3. Book at different time → should succeed
# 4. Filter appointments by date
# 5. Cancel appointment
# 6. Update appointment time

# 💡 ADVANCED FEATURES:
# - Recurring appointments
# - Waitlist management
# - No-show tracking
# - Automated reminders (email/SMS)
# - Calendar sync (Google Calendar, etc.)

