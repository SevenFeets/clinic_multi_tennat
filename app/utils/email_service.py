"""
Email Notification Service
Handles sending email notifications for appointments, reminders, etc.

Uses SendGrid for email delivery.
For free tier: Use Single Sender Verification (verify your personal email)
No domain required!
"""

from typing import Optional
from datetime import datetime, timedelta
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.config import settings

# Import SendGrid (only if available)
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False
    print("[WARNING] SendGrid not installed. Run: pip install sendgrid")


class EmailService:
    """
    Email notification service using SendGrid.
    
    Setup Instructions (NO DOMAIN REQUIRED):
    1. Sign up for free SendGrid account: https://sendgrid.com
    2. Go to Settings → Sender Authentication → Single Sender Verification
    3. Add and verify your personal email (e.g., yourname@gmail.com)
    4. Get API key from Settings → API Keys
    5. Add to .env: SENDGRID_API_KEY=your_key_here
    6. Set EMAIL_FROM_ADDRESS to your verified email in .env
    """
    
    def __init__(self):
        self.enabled = settings.email_enabled
        
        # Initialize SendGrid client if API key is provided
        if SENDGRID_AVAILABLE and settings.sendgrid_api_key:
            try:
                self.sendgrid_client = SendGridAPIClient(settings.sendgrid_api_key)
                self.sendgrid_configured = True
                print("[EMAIL] SendGrid initialized successfully")
            except Exception as e:
                print(f"[EMAIL ERROR] Failed to initialize SendGrid: {e}")
                self.sendgrid_configured = False
        else:
            self.sendgrid_configured = False
            if not SENDGRID_AVAILABLE:
                print("[EMAIL] SendGrid package not installed")
            elif not settings.sendgrid_api_key:
                print("[EMAIL] SendGrid API key not configured")
    
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
        
        # Send email using SendGrid
        try:
            if not self.sendgrid_configured:
                print(f"[EMAIL] SendGrid not configured. Would send reminder to {recipient_email}")
                return False
            
            # Create SendGrid mail message
            message = Mail(
                from_email=settings.email_from_address,
                to_emails=recipient_email,
                subject=subject,
                html_content=body
            )
            
            # Send email
            response = self.sendgrid_client.send(message)
            
            # Check if successful (202 = accepted)
            if response.status_code == 202:
                print(f"[EMAIL] Reminder sent successfully to {recipient_email}")
                return True
            else:
                print(f"[EMAIL ERROR] SendGrid returned status {response.status_code}")
                return False
                
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
            if not self.sendgrid_configured:
                print(f"[EMAIL] SendGrid not configured. Would send confirmation to {recipient_email}")
                return False
            
            message = Mail(
                from_email=settings.email_from_address,
                to_emails=recipient_email,
                subject=subject,
                html_content=body
            )
            
            response = self.sendgrid_client.send(message)
            
            if response.status_code == 202:
                print(f"[EMAIL] Confirmation sent successfully to {recipient_email}")
                return True
            else:
                print(f"[EMAIL ERROR] SendGrid returned status {response.status_code}")
                return False
                
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
            if not self.sendgrid_configured:
                print(f"[EMAIL] SendGrid not configured. Would send cancellation to {recipient_email}")
                return False
            
            message = Mail(
                from_email=settings.email_from_address,
                to_emails=recipient_email,
                subject=subject,
                html_content=body
            )
            
            response = self.sendgrid_client.send(message)
            
            if response.status_code == 202:
                print(f"[EMAIL] Cancellation sent successfully to {recipient_email}")
                return True
            else:
                print(f"[EMAIL ERROR] SendGrid returned status {response.status_code}")
                return False
                
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

