
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date, timedelta
from app.database import get_db
from app.models.appointment import Appointment, AppointmentStatus
from app.models.patient import Patient
from app.models.user import User
from app.schemas.appointment import Appointment as AppointmentSchema, AppointmentCreate, AppointmentUpdate
from app.auth.dependencies import get_current_active_user

#create router
router = APIRouter(prefix="/appointments", tags=["Appointments"])


# Helper function to check for time conflicts
def check_time_conflict(
    appointment_time: datetime,
    tenant_id: int,
    duration_minutes: int,
    db: Session,
    exclude_appointment_id: Optional[int] = None,
) -> bool:
    """
    Check if a new appointment conflicts with existing appointments.
    
    Args:
        appointment_time: Start time of the new appointment
        tenant_id: Tenant ID to filter appointments
        duration_minutes: Duration of the new appointment
        db: Database session
        exclude_appointment_id: Optional ID to exclude (for updates)
    
    Returns:
        True if conflict exists, False otherwise
    """
    new_start_time = appointment_time
    new_end_time = appointment_time + timedelta(minutes=duration_minutes)
    
    # Get all active appointments for the same tenant
    query = db.query(Appointment).filter(
        Appointment.tenant_id == tenant_id,
        Appointment.status != AppointmentStatus.cancelled,
    )

    if exclude_appointment_id:
        query = query.filter(Appointment.id != exclude_appointment_id)

    appointments = query.all()

    # Check each appointment for time overlap
    for appointment in appointments:
        existing_start_time = appointment.appointment_time
        existing_end_time = appointment.appointment_time + timedelta(minutes=appointment.duration_minutes)

        # Two appointments overlap if:
        # new_start < existing_end AND new_end > existing_start
        if new_start_time < existing_end_time and new_end_time > existing_start_time:
            return True  # Conflict found

    return False  # No conflicts


# Helper function to validate business hours
def is_within_business_hours(appointment_time: datetime, duration_minutes: int) -> bool:
    """
    Check if appointment falls within business hours (9 AM - 5 PM).
    
    Args:
        appointment_time: Start time of the appointment
        duration_minutes: Duration of the appointment
    
    Returns:
        True if within business hours, False otherwise
    """
    BUSINESS_START_HOUR = 9  # 9 AM
    BUSINESS_END_HOUR = 17   # 5 PM
    
    start_hour = appointment_time.hour
    end_time = appointment_time + timedelta(minutes=duration_minutes)
    end_hour = end_time.hour
    end_minute = end_time.minute
    
    # Check if start is within business hours
    if start_hour < BUSINESS_START_HOUR or start_hour >= BUSINESS_END_HOUR:
        return False
    
    # Check if end is within business hours
    # Allow exact 5 PM end time
    if end_hour > BUSINESS_END_HOUR or (end_hour == BUSINESS_END_HOUR and end_minute > 0):
        return False
    
    return True


# Helper function to validate appointment is in the future
def is_future_appointment(appointment_time: datetime) -> bool:
    """
    Check if appointment is scheduled for the future.
    
    Args:
        appointment_time: Start time of the appointment
    
    Returns:
        True if appointment is in the future, False otherwise
    """
    return appointment_time > datetime.now()


# create appointment endpoint
@router.post("/", response_model=AppointmentSchema, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
    ):

     # Verify patient belongs to same tenant
    patient = db.query(Patient).filter(
        Patient.id == appointment_data.patient_id,
        Patient.tenant_id == current_user.tenant_id
    ).first()

    # If patient not found, raise 404 error
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    # Validate appointment is in the future
    if not is_future_appointment(appointment_data.appointment_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment must be scheduled for a future date and time"
        )

    # Validate business hours
    if not is_within_business_hours(appointment_data.appointment_time, appointment_data.duration_minutes):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment must be within business hours (9 AM - 5 PM)"
        )

    # Check for time conflicts
    if check_time_conflict(
        appointment_data.appointment_time,
        current_user.tenant_id,
        appointment_data.duration_minutes,
        db,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time slot is already booked. Please choose another time."
        )

    # Create appointment
    new_appointment = Appointment(
        **appointment_data.model_dump(),
        tenant_id=current_user.tenant_id,
        patient_id=patient.id,
        status=AppointmentStatus.scheduled
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment



# Get appointments endpoint (with filters)
@router.get("/", response_model=List[AppointmentSchema])
async def get_appointments(
    skip: int = 0,
    limit: int = 100,
    patient_id: Optional[int] = None,
    status: Optional[AppointmentStatus] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
    ):

    # Base query with tenant filter
    query = db.query(Appointment).filter(
        Appointment.tenant_id == current_user.tenant_id
    )

    # Apply optional filters
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    if status:
        query = query.filter(Appointment.status == status)
    if date_from:
        query = query.filter(Appointment.appointment_time >= date_from)
    if date_to:
        query = query.filter(Appointment.appointment_time <= date_to)
    # Execute query with pagination
    appointments = query.offset(skip).limit(limit).all()
    return appointments


# Get single appointment endpoint
@router.get("/{appointment_id}", response_model=AppointmentSchema)
async def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
    ):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.tenant_id == current_user.tenant_id
    ).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment



# Update appointment endpoint
@router.patch("/{appointment_id}", response_model=AppointmentSchema)
async def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
    ):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.tenant_id == current_user.tenant_id
    ).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

    # Update only provided fields
    update_data = appointment_data.model_dump(exclude_unset=True)

    # If time or duration is changed, validate the new schedule
    if 'appointment_time' in update_data or 'duration_minutes' in update_data:   
        new_time = update_data.get('appointment_time', appointment.appointment_time)
        new_duration = update_data.get('duration_minutes', appointment.duration_minutes)

        # Validate appointment is in the future
        if not is_future_appointment(new_time):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment must be scheduled for a future date and time"
            )

        # Validate business hours
        if not is_within_business_hours(new_time, new_duration):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment must be within business hours (9 AM - 5 PM)"
            )

        # Check for time conflicts (excluding current appointment)
        if check_time_conflict(
            new_time,
            current_user.tenant_id,
            new_duration,
            db,
            exclude_appointment_id=appointment.id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time slot is already booked. Please choose another time."
            )

    # update appointment
    for field, value in update_data.items():
        setattr(appointment, field, value)

    db.commit()
    db.refresh(appointment)
    return appointment


# Cancel appointment endpoint
@router.post("/{appointment_id}/cancel", response_model=AppointmentSchema)
async def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
    ):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.tenant_id == current_user.tenant_id
    ).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

    appointment.status = AppointmentStatus.cancelled
    db.commit()
    db.refresh(appointment)
    return appointment




# TODO: more basic features:

# - Send appointment reminders
# - Calculate appointment statistics

# TODO: ADVANCED FEATURES:
# - Recurring appointments
# - Waitlist management
# - No-show tracking
# - Automated reminders (email/SMS)
# - Calendar sync (Google Calendar, etc.)


# IMPORTANT:
# - Use timezone-aware datetimes
# - Handle daylight saving time
# - Consider different time zones (future)
# - Add proper indexes on appointment_time

#  TESTING:
# 1. Book an appointment
# 2. Try booking at same time → should fail
# 3. Book at different time → should succeed
# 4. Filter appointments by date
# 5. Cancel appointment
# 6. Update appointment time


