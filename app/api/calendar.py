"""
Google Calendar Integration API
Handles OAuth2 flow and calendar event synchronization
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.models.appointment import Appointment
from app.models.tenant import Tenant
from app.auth.dependencies import get_current_active_user, get_tenant
from app.services.calendar_service import calendar_service

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get("/authorize")
async def authorize_calendar(
    current_user: User = Depends(get_current_active_user),
    tenant: Tenant = Depends(get_tenant)
):
    """
    Start Google Calendar OAuth2 authorization flow.
    
    Returns authorization URL that user should visit to grant permissions.
    After authorization, user will be redirected to callback endpoint.
    """
    if not calendar_service.enabled:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google Calendar integration not configured"
        )
    
    try:
        authorization_url, flow = calendar_service.get_authorization_url(tenant.id)
        
        # TODO: Store flow object temporarily (in session/cache)
        # HINT: Use request.session or Redis cache
        # HINT: Key could be f"oauth_flow_{tenant.id}"
        # HINT: Store flow object (may need to serialize it)
        
        return {
            "authorization_url": authorization_url,
            "message": "Visit the authorization_url to grant calendar access"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating authorization URL: {str(e)}"
        )


@router.get("/callback")
async def calendar_callback(
    code: str,
    state: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle OAuth2 callback from Google.
    
    This endpoint is called by Google after user grants permission.
    Exchanges authorization code for access tokens.
    """
    try:
        # TODO: Retrieve flow object from session/cache
        # HINT: Use the state parameter to identify tenant
        # HINT: Extract tenant_id from state (e.g., "tenant_1")
        
        tenant_id = None  # Extract from state
        flow = None  # Retrieve from cache
        
        if not flow:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OAuth flow not found. Please start authorization again."
            )
        
        # Exchange code for tokens
        tokens = calendar_service.exchange_code_for_tokens(code, flow)
        
        # TODO: Store tokens in database
        # HINT: Update tenant model with tokens
        # HINT: Encrypt tokens before storing!
        # HINT: Store: access_token, refresh_token, expires_at
        
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if tenant:
            # TODO: Store encrypted tokens
            # tenant.google_calendar_token = encrypt(tokens['token'])
            # tenant.google_calendar_refresh_token = encrypt(tokens['refresh_token'])
            # tenant.google_calendar_enabled = True
            db.commit()
        
        return {
            "message": "Calendar connected successfully",
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing callback: {str(e)}"
        )


@router.post("/appointments/{appointment_id}/sync")
async def sync_appointment_to_calendar(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user),
    tenant: Tenant = Depends(get_tenant),
    db: Session = Depends(get_db)
):
    """
    Sync a specific appointment to Google Calendar.
    
    Creates or updates calendar event for the appointment.
    """
    # Get appointment
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.tenant_id == tenant.id
    ).first()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # TODO: Get tenant's Google Calendar token
    # HINT: tenant.google_calendar_token (decrypt if encrypted)
    access_token = None  # Get from tenant
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google Calendar not connected. Please authorize first."
        )
    
    # Create/update calendar event
    if appointment.google_calendar_event_id:
        # Update existing event
        success = calendar_service.update_calendar_event(
            appointment.google_calendar_event_id,
            appointment,
            access_token
        )
    else:
        # Create new event
        event_id = calendar_service.create_calendar_event(
            appointment,
            access_token
        )
        if event_id:
            appointment.google_calendar_event_id = event_id
            db.commit()
            success = True
        else:
            success = False
    
    if success:
        return {"message": "Appointment synced to calendar", "status": "success"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to sync appointment to calendar"
        )


@router.delete("/disconnect")
async def disconnect_calendar(
    current_user: User = Depends(get_current_active_user),
    tenant: Tenant = Depends(get_tenant),
    db: Session = Depends(get_db)
):
    """
    Disconnect Google Calendar integration.
    
    Removes stored tokens and disables calendar sync.
    """
    # TODO: Clear tenant's calendar tokens
    # tenant.google_calendar_token = None
    # tenant.google_calendar_refresh_token = None
    # tenant.google_calendar_enabled = False
    db.commit()
    
    return {"message": "Calendar disconnected successfully"}


# 📖 UNDERSTANDING OAUTH2 FLOW:
#
# 1. User clicks "Connect Calendar"
# 2. Backend generates authorization_url
# 3. User redirected to Google login
# 4. User grants permissions
# 5. Google redirects to /callback with code
# 6. Backend exchanges code for tokens
# 7. Store tokens securely
# 8. Use tokens for API calls
#
# Security:
# - Always encrypt tokens in database
# - Use HTTPS in production
# - Validate state parameter
# - Handle token expiration

