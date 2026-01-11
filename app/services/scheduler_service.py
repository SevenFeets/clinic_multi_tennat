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

scheduler = BackgroundScheduler()


def check_and_send_reminders():
    """Background job that checks for appointments needing reminders."""
    db = SessionLocal()
    try:
        now = datetime.now()
        reminder_window_start = now + timedelta(hours=23)
        reminder_window_end = now + timedelta(hours=25)
        
        # TODO: Query appointments in reminder window
        appointments_to_remind = []
        
        for appointment in appointments_to_remind:
            try:
                # TODO: Get patient for this appointment
                
                patient = None
                
                if patient and patient.owner_email:
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
        scheduler.add_job(
            check_and_send_reminders,
            trigger=CronTrigger(minute=0),
            id='send_appointment_reminders',
            name='Send appointment reminders',
            replace_existing=True,
            max_instances=1
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

# UNDERSTANDING APSCHEDULER:
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


