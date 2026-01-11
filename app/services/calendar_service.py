"""
Google Calendar Service
Handles OAuth2 authentication and calendar event synchronization

USAGE:
1. User authorizes via OAuth2
2. Store access token
3. Use token to create/update calendar events
"""

from typing import Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.config import settings
from app.models.appointment import Appointment
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']


class CalendarService:
    """Service for Google Calendar integration."""
    
    def __init__(self):
        """Initialize calendar service with OAuth2 config"""
        if not settings.google_client_id or not settings.google_client_secret:
            logger.warning("Google Calendar credentials not configured")
            self.enabled = False
        else:
            self.enabled = True
            self.client_config = {
                "web": {
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [settings.google_redirect_uri]
                }
            }
    
    def get_authorization_url(self, tenant_id: int, state: Optional[str] = None) -> tuple[str, Flow]:
        """Generate OAuth2 authorization URL."""
        if not self.enabled:
            raise ValueError("Google Calendar not configured")
        
        flow = Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            redirect_uri=settings.google_redirect_uri
        )
        
        state_data = state or f"tenant_{tenant_id}"
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state_data,
            prompt='consent'
        )
        
        return authorization_url, flow
    
    def exchange_code_for_tokens(self, code: str, flow: Flow) -> dict:
        """Exchange authorization code for access and refresh tokens."""
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        return {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'expiry': credentials.expiry.isoformat() if credentials.expiry else None
        }
    
    def create_calendar_event(
        self,
        appointment: Appointment,
        access_token: str,
        calendar_id: str = 'primary'
    ) -> Optional[str]:
        """Create a calendar event for an appointment."""
        try:
            credentials = Credentials(token=access_token)
            service = build('calendar', 'v3', credentials=credentials)
            
            end_time = appointment.appointment_time + timedelta(minutes=appointment.duration_minutes)
            
            patient = appointment.patient
            patient_name = patient.pet_name if hasattr(patient, 'pet_name') else f"Patient {patient.id}"
            
            event = {
                'summary': f'Appointment: {patient_name}',
                'description': appointment.notes or f'Appointment for {patient_name}',
                'start': {
                    'dateTime': appointment.appointment_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 60},
                    ],
                },
            }
            
            created_event = service.events().insert(
                calendarId=calendar_id,
                body=event
            ).execute()
            
            logger.info(f"Created calendar event {created_event['id']} for appointment {appointment.id}")
            return created_event['id']
            
        except HttpError as e:
            logger.error(f"Error creating calendar event: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating calendar event: {e}")
            return None
    
    def update_calendar_event(
        self,
        event_id: str,
        appointment: Appointment,
        access_token: str,
        calendar_id: str = 'primary'
    ) -> bool:
        """Update an existing calendar event."""
        # TODO: Implement event update
        # HINT: Use service.events().update() instead of insert()
        return False
    
    def delete_calendar_event(
        self,
        event_id: str,
        access_token: str,
        calendar_id: str = 'primary'
    ) -> bool:
        """Delete a calendar event."""
        # TODO: Implement event deletion
        return False


calendar_service = CalendarService()
