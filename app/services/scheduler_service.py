"""
Background Job Scheduler Service
Handles automated tasks like sending appointment reminders

USAGE:
- Scheduler runs in background
- Jobs execute at scheduled intervals
- Perfect for sending reminders automatically
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.database import SessionLocal
from app.models.appointment import Appointment, AppointmentStatus
from app.models.patient import Patient
from app.utils.email_service import email_service
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Create scheduler instance
scheduler = BackgroundScheduler()


def check_and_send_reminders():
    """
    Background job that checks for appointments needing reminders.
    
    Runs every hour and sends reminders for appointments scheduled
    in the next 24 hours.
    
    TODO: Implement the logic:
    1. Get current time + 24 hours (reminder window)
    2. Query appointments that:
       - Are scheduled (status = scheduled)
       - Are in the reminder window (24h from now)
       - Haven't had reminder sent yet (reminder_sent_at is None)
    3. For each appointment:
       - Get the patient
       - Send reminder email
       - Update reminder_sent_at timestamp
    """
    db = SessionLocal()
    try:
        now = datetime.now()
        reminder_window_start = now + timedelta(hours=23)  # 23 hours from now
        reminder_window_end = now + timedelta(hours=25)    # 25 hours from now
        
        # TODO: Query appointments in reminder window
        # HINT: Use db.query(Appointment).filter(...)
        # HINT: Filter by:
        #   - status == AppointmentStatus.scheduled
        #   - appointment_time between reminder_window_start and reminder_window_end
        #   - reminder_sent_at is None (or doesn't exist yet)
        #   - tenant_id (you'll need to iterate through tenants or pass tenant_id)
        
        appointments_to_remind = []  # Replace with actual query
        
        for appointment in appointments_to_remind:
            try:
                # TODO: Get patient for this appointment
                # HINT: db.query(Patient).filter(Patient.id == appointment.patient_id).first()
                
                patient = None  # Replace with actual query
                
                if patient and patient.owner_email:
                    # Send reminder (use asyncio.run for async function in sync context)
                    import asyncio
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    success = loop.run_until_complete(
                        email_service.send_appointment_reminder(
                            appointment,
                            patient,
                            reminder_hours=24
                        )
                    )
                    
                    if success:
                        # TODO: Mark reminder as sent
                        # HINT: appointment.reminder_sent_at = now
                        # HINT: db.commit()
                        logger.info(f"Reminder sent for appointment {appointment.id}")
                    else:
                        logger.warning(f"Failed to send reminder for appointment {appointment.id}")
                else:
                    logger.warning(f"No email for appointment {appointment.id}")
                    
            except Exception as e:
                logger.error(f"Error sending reminder for appointment {appointment.id}: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error in reminder job: {e}")
    finally:
        db.close()


def start_scheduler():
    """Start the background scheduler"""
    if not scheduler.running:
        # Schedule reminder job to run every hour at minute 0
        scheduler.add_job(
            check_and_send_reminders,
            trigger=CronTrigger(minute=0),  # Run at top of every hour
            id='send_appointment_reminders',
            name='Send appointment reminders',
            replace_existing=True,
            max_instances=1  # Only one instance at a time
        )
        
        scheduler.start()
        logger.info("Background scheduler started - reminders will run hourly")
    else:
        logger.warning("Scheduler is already running")


def stop_scheduler():
    """Stop the background scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Background scheduler stopped")
    else:
        logger.warning("Scheduler is not running")


# 📖 UNDERSTANDING APSCHEDULER:
#
# CronTrigger patterns:
# - minute=0 → Run at top of every hour
# - hour=9, minute=0 → Run daily at 9 AM
# - day_of_week='mon', hour=9 → Run every Monday at 9 AM
#
# Other triggers:
# - IntervalTrigger(hours=1) → Every hour
# - DateTrigger(run_date=datetime) → Run once at specific time
#
# Job options:
# - max_instances=1 → Prevent overlapping jobs
# - replace_existing=True → Update job if it exists
# - coalesce=True → Combine multiple pending runs into one

