"""
Waitlist Management API
Handles waitlist entries for appointment scheduling
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.waitlist import Waitlist
from app.models.patient import Patient
from app.models.user import User
from app.schemas.waitlist import Waitlist as WaitlistSchema, WaitlistCreate, WaitlistUpdate
from app.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/waitlist", tags=["Waitlist"])


@router.post("/", response_model=WaitlistSchema, status_code=status.HTTP_201_CREATED)
async def create_waitlist_entry(
    waitlist_data: WaitlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Add a patient to the waitlist for a desired appointment time.
    """
    # Verify patient belongs to same tenant
    patient = db.query(Patient).filter(
        Patient.id == waitlist_data.patient_id,
        Patient.tenant_id == current_user.tenant_id
    ).first()
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Check if patient already has an active waitlist entry for similar time
    existing_entry = db.query(Waitlist).filter(
        Waitlist.patient_id == waitlist_data.patient_id,
        Waitlist.tenant_id == current_user.tenant_id,
        Waitlist.is_active == True,
        Waitlist.desired_date == waitlist_data.desired_date.date()
    ).first()
    
    if existing_entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Patient already has an active waitlist entry for this date"
        )
    
    # Create waitlist entry
    new_entry = Waitlist(
        **waitlist_data.model_dump(),
        tenant_id=current_user.tenant_id
    )
    
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.get("/", response_model=List[WaitlistSchema])
async def get_waitlist(
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all waitlist entries for the current tenant.
    By default, returns only active entries.
    """
    query = db.query(Waitlist).filter(
        Waitlist.tenant_id == current_user.tenant_id
    )
    
    if active_only:
        query = query.filter(Waitlist.is_active == True)
    
    # Order by priority (highest first), then by creation date
    entries = query.order_by(
        Waitlist.priority.desc(),
        Waitlist.created_at.asc()
    ).all()
    
    return entries


@router.get("/{waitlist_id}", response_model=WaitlistSchema)
async def get_waitlist_entry(
    waitlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific waitlist entry"""
    entry = db.query(Waitlist).filter(
        Waitlist.id == waitlist_id,
        Waitlist.tenant_id == current_user.tenant_id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waitlist entry not found"
        )
    
    return entry


@router.patch("/{waitlist_id}", response_model=WaitlistSchema)
async def update_waitlist_entry(
    waitlist_id: int,
    waitlist_data: WaitlistUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a waitlist entry"""
    entry = db.query(Waitlist).filter(
        Waitlist.id == waitlist_id,
        Waitlist.tenant_id == current_user.tenant_id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waitlist entry not found"
        )
    
    # Update only provided fields
    update_data = waitlist_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)
    
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{waitlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_waitlist_entry(
    waitlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a waitlist entry (or mark as inactive).
    """
    entry = db.query(Waitlist).filter(
        Waitlist.id == waitlist_id,
        Waitlist.tenant_id == current_user.tenant_id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waitlist entry not found"
        )
    
    # Soft delete: mark as inactive instead of hard delete
    entry.is_active = False
    db.commit()
    return None


@router.post("/{waitlist_id}/fulfill", response_model=WaitlistSchema)
async def fulfill_waitlist_entry(
    waitlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mark a waitlist entry as fulfilled.
    This should be called when an appointment is created from the waitlist.
    """
    entry = db.query(Waitlist).filter(
        Waitlist.id == waitlist_id,
        Waitlist.tenant_id == current_user.tenant_id
    ).first()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Waitlist entry not found"
        )
    
    entry.is_active = False
    entry.fulfilled_at = datetime.now()
    db.commit()
    db.refresh(entry)
    return entry

