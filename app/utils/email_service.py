"""
Email Notification Service
Handles sending email notifications for appointments, reminders, etc.

For production, integrate with:
- SendGrid
- AWS SES
- Mailgun
- SMTP server
"""

from typing import Optional
from datetime import datetime, timedelta
from app.models.appointment import Appointment
from app.models.patient import Patient


class EmailService:
    """
    Email notification service.
    
    Currently a placeholder that logs emails.
    In production, integrate with a real email service.
    """
    
    def __init__(self):
        # In production, initialize your email service here
        # Example: self.sendgrid_client = SendGridAPIClient(api_key=settings.sendgrid_api_key)
        self.enabled = True  # Set to False to disable emails
    
    async def send_appointment_reminder(
        self,
        appointment: Appointment,
        patient: Patient,
        reminder_hours: int = 24
    ) -> bool:
        """
        Send appointment reminder email to patient.
        
        Args:
            appointment: The appointment to remind about
            patient: The patient (pet owner) to notify
            reminder_hours: How many hours before appointment to send reminder
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.enabled:
            return False
        
        # Check if reminder should be sent (e.g., 24 hours before)
        appointment_time = appointment.appointment_time
        reminder_time = appointment_time - timedelta(hours=reminder_hours)
        now = datetime.now()
        
        # Only send if we're within the reminder window
        if now < reminder_time or now > appointment_time:
            return False
        
        # Get patient email
        recipient_email = patient.owner_email
        if not recipient_email:
            # No email address, can't send
            return False
        
        # Prepare email content
        subject = f"Appointment Reminder: {appointment_time.strftime('%B %d, %Y at %I:%M %p')}"
        body = self._generate_reminder_email_body(appointment, patient)
        
        # Send email (placeholder - replace with actual email service)
        try:
            # TODO: Replace with actual email sending
            # Example with SendGrid:
            # message = Mail(
            #     from_email='noreply@clinic.com',
            #     to_emails=recipient_email,
            #     subject=subject,
            #     html_content=body
            # )
            # response = self.sendgrid_client.send(message)
            
            # For now, just log it
            print(f"[EMAIL] Would send reminder to {recipient_email}")
            print(f"[EMAIL] Subject: {subject}")
            print(f"[EMAIL] Body: {body[:100]}...")
            
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send reminder: {e}")
            return False
    
    async def send_appointment_confirmation(
        self,
        appointment: Appointment,
        patient: Patient
    ) -> bool:
        """Send appointment confirmation email"""
        if not self.enabled:
            return False
        
        recipient_email = patient.owner_email
        if not recipient_email:
            return False
        
        subject = f"Appointment Confirmed: {appointment.appointment_time.strftime('%B %d, %Y at %I:%M %p')}"
        body = self._generate_confirmation_email_body(appointment, patient)
        
        try:
            # TODO: Replace with actual email sending
            print(f"[EMAIL] Would send confirmation to {recipient_email}")
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send confirmation: {e}")
            return False
    
    async def send_appointment_cancellation(
        self,
        appointment: Appointment,
        patient: Patient
    ) -> bool:
        """Send appointment cancellation email"""
        if not self.enabled:
            return False
        
        recipient_email = patient.owner_email
        if not recipient_email:
            return False
        
        subject = f"Appointment Cancelled: {appointment.appointment_time.strftime('%B %d, %Y at %I:%M %p')}"
        body = self._generate_cancellation_email_body(appointment, patient)
        
        try:
            # TODO: Replace with actual email sending
            print(f"[EMAIL] Would send cancellation to {recipient_email}")
            return True
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send cancellation: {e}")
            return False
    
    def _generate_reminder_email_body(self, appointment: Appointment, patient: Patient) -> str:
        """Generate HTML email body for appointment reminder"""
        appointment_time = appointment.appointment_time
        return f"""
        <html>
        <body>
            <h2>Appointment Reminder</h2>
            <p>Dear {patient.owner_first_name},</p>
            <p>This is a reminder that you have an appointment scheduled:</p>
            <ul>
                <li><strong>Pet:</strong> {patient.pet_name}</li>
                <li><strong>Date & Time:</strong> {appointment_time.strftime('%B %d, %Y at %I:%M %p')}</li>
                <li><strong>Duration:</strong> {appointment.duration_minutes} minutes</li>
            </ul>
            <p>Please arrive 10 minutes early.</p>
            <p>If you need to reschedule or cancel, please contact us.</p>
            <p>Best regards,<br>Clinic Team</p>
        </body>
        </html>
        """
    
    def _generate_confirmation_email_body(self, appointment: Appointment, patient: Patient) -> str:
        """Generate HTML email body for appointment confirmation"""
        appointment_time = appointment.appointment_time
        return f"""
        <html>
        <body>
            <h2>Appointment Confirmed</h2>
            <p>Dear {patient.owner_first_name},</p>
            <p>Your appointment has been confirmed:</p>
            <ul>
                <li><strong>Pet:</strong> {patient.pet_name}</li>
                <li><strong>Date & Time:</strong> {appointment_time.strftime('%B %d, %Y at %I:%M %p')}</li>
                <li><strong>Duration:</strong> {appointment.duration_minutes} minutes</li>
            </ul>
            <p>We look forward to seeing you!</p>
            <p>Best regards,<br>Clinic Team</p>
        </body>
        </html>
        """
    
    def _generate_cancellation_email_body(self, appointment: Appointment, patient: Patient) -> str:
        """Generate HTML email body for appointment cancellation"""
        appointment_time = appointment.appointment_time
        return f"""
        <html>
        <body>
            <h2>Appointment Cancelled</h2>
            <p>Dear {patient.owner_first_name},</p>
            <p>Your appointment has been cancelled:</p>
            <ul>
                <li><strong>Pet:</strong> {patient.pet_name}</li>
                <li><strong>Date & Time:</strong> {appointment_time.strftime('%B %d, %Y at %I:%M %p')}</li>
            </ul>
            <p>If you would like to reschedule, please contact us.</p>
            <p>Best regards,<br>Clinic Team</p>
        </body>
        </html>
        """


# Global email service instance
email_service = EmailService()

