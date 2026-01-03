"""
Recurring Appointments API
Manages recurring appointment templates
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models.recurring_appointment import RecurringAppointment, RecurrencePattern
from app.models.patient import Patient
from app.models.appointment import Appointment, AppointmentStatus
from app.models.user import User
from app.schemas.recurring_appointment import (
    RecurringAppointment as RecurringAppointmentSchema,
    RecurringAppointmentCreate,
    RecurringAppointmentUpdate
)
from app.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/recurring-appointments", tags=["Recurring Appointments"])


@router.post("/", response_model=RecurringAppointmentSchema, status_code=status.HTTP_201_CREATED)
async def create_recurring_appointment(
    recurring_data: RecurringAppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a recurring appointment template.
    This will generate individual appointments based on the pattern.
    """
    # Verify patient belongs to same tenant
    patient = db.query(Patient).filter(
        Patient.id == recurring_data.patient_id,
        Patient.tenant_id == current_user.tenant_id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Create recurring appointment template
    new_recurring = RecurringAppointment(
        **recurring_data.model_dump(),
        tenant_id=current_user.tenant_id
    )
    
    db.add(new_recurring)
    db.commit()
    db.refresh(new_recurring)
    
    # Generate initial appointments from the template
    # This is a simplified version - in production, you'd use a background job
    await generate_appointments_from_template(new_recurring.id, db, current_user)
    
    return new_recurring


@router.get("/", response_model=List[RecurringAppointmentSchema])
async def get_recurring_appointments(
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all recurring appointment templates"""
    query = db.query(RecurringAppointment).filter(
        RecurringAppointment.tenant_id == current_user.tenant_id
    )
    
    if active_only:
        query = query.filter(RecurringAppointment.is_active == True)
    
    return query.all()


@router.get("/{recurring_id}", response_model=RecurringAppointmentSchema)
async def get_recurring_appointment(
    recurring_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific recurring appointment template"""
    recurring = db.query(RecurringAppointment).filter(
        RecurringAppointment.id == recurring_id,
        RecurringAppointment.tenant_id == current_user.tenant_id
    ).first()
    
    if not recurring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring appointment not found"
        )
    
    return recurring


@router.patch("/{recurring_id}", response_model=RecurringAppointmentSchema)
async def update_recurring_appointment(
    recurring_id: int,
    recurring_data: RecurringAppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a recurring appointment template"""
    recurring = db.query(RecurringAppointment).filter(
        RecurringAppointment.id == recurring_id,
        RecurringAppointment.tenant_id == current_user.tenant_id
    ).first()
    
    if not recurring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring appointment not found"
        )
    
    update_data = recurring_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(recurring, field, value)
    
    db.commit()
    db.refresh(recurring)
    return recurring


@router.delete("/{recurring_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recurring_appointment(
    recurring_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete (deactivate) a recurring appointment template"""
    recurring = db.query(RecurringAppointment).filter(
        RecurringAppointment.id == recurring_id,
        RecurringAppointment.tenant_id == current_user.tenant_id
    ).first()
    
    if not recurring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring appointment not found"
        )
    
    # Soft delete: mark as inactive
    recurring.is_active = False
    db.commit()
    return None


@router.post("/{recurring_id}/generate", status_code=status.HTTP_200_OK)
async def generate_appointments(
    recurring_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Manually trigger generation of appointments from a recurring template.
    This is useful for generating appointments in advance.
    """
    recurring = db.query(RecurringAppointment).filter(
        RecurringAppointment.id == recurring_id,
        RecurringAppointment.tenant_id == current_user.tenant_id
    ).first()
    
    if not recurring:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring appointment not found"
        )
    
    generated_count = await generate_appointments_from_template(recurring_id, db, current_user)
    
    return {"message": f"Generated {generated_count} appointments", "count": generated_count}


async def generate_appointments_from_template(
    recurring_id: int,
    db: Session,
    current_user: User,
    days_ahead: int = 90  # Generate appointments for next 90 days
) -> int:
    """
    Helper function to generate individual appointments from a recurring template.
    This is a simplified version - in production, use a background job scheduler.
    """
    recurring = db.query(RecurringAppointment).filter(
        RecurringAppointment.id == recurring_id
    ).first()
    
    if not recurring or not recurring.is_active:
        return 0
    
    now = datetime.now()
    end_date = recurring.end_date if recurring.end_date else (now + timedelta(days=days_ahead))
    current_date = max(recurring.start_date, now)
    
    # Parse time_of_day
    hour, minute = map(int, recurring.time_of_day.split(':'))
    
    generated_count = 0
    
    while current_date <= end_date and current_date <= (now + timedelta(days=days_ahead)):
        # Create appointment datetime
        appointment_time = current_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Skip if appointment is in the past
        if appointment_time <= now:
            # Move to next occurrence
            current_date = _get_next_occurrence(current_date, recurring.pattern, recurring.interval)
            continue
        
        # Check if appointment already exists
        existing = db.query(Appointment).filter(
            Appointment.tenant_id == recurring.tenant_id,
            Appointment.patient_id == recurring.patient_id,
            Appointment.appointment_time == appointment_time
        ).first()
        
        if not existing:
            # Create new appointment
            new_appointment = Appointment(
                tenant_id=recurring.tenant_id,
                patient_id=recurring.patient_id,
                appointment_time=appointment_time,
                duration_minutes=recurring.duration_minutes,
                status=AppointmentStatus.scheduled,
                notes=recurring.notes
            )
            db.add(new_appointment)
            generated_count += 1
        
        # Move to next occurrence
        current_date = _get_next_occurrence(current_date, recurring.pattern, recurring.interval)
    
    # Update last_generated timestamp
    recurring.last_generated = now
    db.commit()
    
    return generated_count


def _get_next_occurrence(current_date: datetime, pattern: RecurrencePattern, interval: int) -> datetime:
    """Calculate the next occurrence date based on pattern"""
    if pattern == RecurrencePattern.daily:
        return current_date + timedelta(days=interval)
    elif pattern == RecurrencePattern.weekly:
        return current_date + timedelta(weeks=interval)
    elif pattern == RecurrencePattern.monthly:
        # Simple monthly: add 30 days (for production, use proper month calculation)
        return current_date + timedelta(days=30 * interval)
    elif pattern == RecurrencePattern.yearly:
        return current_date + timedelta(days=365 * interval)
    else:
        return current_date + timedelta(days=1)

