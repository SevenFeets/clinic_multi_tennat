"""
Dashboard Statistics Endpoint
Provides aggregated statistics for the dashboard
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta, date
from app.database import get_db
from app.models.patient import Patient
from app.models.appointment import Appointment, AppointmentStatus
from app.models.user import User
from app.auth.dependencies import get_current_active_user
from pydantic import BaseModel

# Create router
router = APIRouter(prefix="/stats", tags=["Statistics"])


# Response model for stats
class DashboardStats(BaseModel):
    total_patients: int
    patients_this_month: int
    today_appointments: int
    today_completed: int
    pending_appointments: int
    revenue_this_month: float
    
    class Config:
        from_attributes = True


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all statistics for the dashboard in one request.
    All data is filtered by the current user's tenant.
    """
    
    # Get current date/time for filtering
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day, 0, 0, 0)
    today_end = datetime(now.year, now.month, now.day, 23, 59, 59)
    
    # First day of current month
    month_start = datetime(now.year, now.month, 1, 0, 0, 0)
    
    # 1. Total patients count
    total_patients = db.query(func.count(Patient.id)).filter(
        Patient.tenant_id == current_user.tenant_id
    ).scalar() or 0
    
    # 2. Patients added this month
    patients_this_month = db.query(func.count(Patient.id)).filter(
        Patient.tenant_id == current_user.tenant_id,
        Patient.created_at >= month_start
    ).scalar() or 0
    
    # 3. Today's appointments (all statuses)
    today_appointments = db.query(func.count(Appointment.id)).filter(
        Appointment.tenant_id == current_user.tenant_id,
        Appointment.appointment_time >= today_start,
        Appointment.appointment_time <= today_end
    ).scalar() or 0
    
    # 4. Today's completed appointments
    today_completed = db.query(func.count(Appointment.id)).filter(
        Appointment.tenant_id == current_user.tenant_id,
        Appointment.appointment_time >= today_start,
        Appointment.appointment_time <= today_end,
        Appointment.status == AppointmentStatus.completed
    ).scalar() or 0
    
    # 5. Pending appointments (scheduled for future)
    pending_appointments = db.query(func.count(Appointment.id)).filter(
        Appointment.tenant_id == current_user.tenant_id,
        Appointment.status == AppointmentStatus.scheduled,
        Appointment.appointment_time > now
    ).scalar() or 0
    
    # 6. Revenue this month (calculated from completed appointments)
    # Assuming each appointment has a cost/fee field (you may need to add this)
    # For now, we'll calculate as: completed_appointments * average_fee
    completed_this_month = db.query(func.count(Appointment.id)).filter(
        Appointment.tenant_id == current_user.tenant_id,
        Appointment.status == AppointmentStatus.completed,
        Appointment.appointment_time >= month_start
    ).scalar() or 0
    
    # TODO: Replace this with actual fee calculation when you add pricing
    # Assuming average appointment fee of $50
    AVERAGE_APPOINTMENT_FEE = 50.0
    revenue_this_month = completed_this_month * AVERAGE_APPOINTMENT_FEE
    
    return DashboardStats(
        total_patients=total_patients,
        patients_this_month=patients_this_month,
        today_appointments=today_appointments,
        today_completed=today_completed,
        pending_appointments=pending_appointments,
        revenue_this_month=revenue_this_month
    )

# 🎯 TODO:
# 1. Add actual revenue tracking (appointment fees)
# 2. Add more stats (average wait time, etc.)
# 3. Add caching for better performance
# 4. Add date range parameters for custom reports




# 📖 UNDERSTANDING THIS ENDPOINT:
# 
# Why one endpoint for all stats?
# - Reduces number of HTTP requests (faster!)
# - Consistent snapshot of data (all from same time)
# - Easier to maintain
#
# SQL Aggregation Functions:
# - func.count() → Count records
# - func.sum() → Sum values
# - func.avg() → Calculate average
# - func.max() → Get maximum value
#
# Date Filtering:
# - Filter by date range using >= and <=
# - Use datetime for precise time comparisons
# - Consider timezone issues in production!




