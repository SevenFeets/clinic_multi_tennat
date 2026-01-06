"""
Appointment Management Tests
Tests for appointment CRUD operations, time conflicts, and business rules
"""
import pytest
from datetime import datetime, timedelta
from app.models.patient import Patient
from app.models.appointment import Appointment


def test_create_appointment(authenticated_client, db_session, test_tenant, test_user):
    """Test creating a new appointment"""
    # Create a patient first
    patient_response = authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Rex",
            "species": "Dog",
            "owner_first_name": "Owner",
            "owner_last_name": "Name"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    patient_id = patient_response.json()["id"]
    
    # Create appointment
    future_time = (datetime.now() + timedelta(days=1)).isoformat()
    response = authenticated_client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "appointment_time": future_time,
            "duration_minutes": 30,
            "notes": "Regular checkup"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["patient_id"] == patient_id
    assert data["duration_minutes"] == 30


def test_get_appointments(authenticated_client, db_session, test_tenant):
    """Test retrieving list of appointments"""
    response = authenticated_client.get(
        "/appointments/",
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_appointment_time_conflict(authenticated_client, db_session, test_tenant):
    """Test that appointments cannot overlap in time"""
    # Create a patient
    patient_response = authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Conflict Test Pet",
            "species": "Cat",
            "owner_first_name": "Test",
            "owner_last_name": "Owner"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    patient_id = patient_response.json()["id"]
    
    # Create first appointment
    appointment_time = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
    response1 = authenticated_client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "appointment_time": appointment_time.isoformat(),
            "duration_minutes": 30
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    assert response1.status_code == 201
    
    # Try to create overlapping appointment
    overlapping_time = appointment_time + timedelta(minutes=15)  # 15 min overlap
    response2 = authenticated_client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "appointment_time": overlapping_time.isoformat(),
            "duration_minutes": 30
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    # Should fail with conflict error
    assert response2.status_code == 400
    assert "conflict" in response2.json()["detail"].lower() or "overlap" in response2.json()["detail"].lower()


def test_appointment_past_time_validation(authenticated_client, db_session, test_tenant):
    """Test that appointments cannot be scheduled in the past"""
    # Create a patient
    patient_response = authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Past Test Pet",
            "species": "Dog",
            "owner_first_name": "Test",
            "owner_last_name": "Owner"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    patient_id = patient_response.json()["id"]
    
    # Try to create appointment in the past
    past_time = (datetime.now() - timedelta(days=1)).isoformat()
    response = authenticated_client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "appointment_time": past_time,
            "duration_minutes": 30
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    # Should fail with validation error
    assert response.status_code == 400


def test_update_appointment_status(authenticated_client, db_session, test_tenant):
    """Test updating appointment status"""
    # Create patient and appointment
    patient_response = authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Status Test Pet",
            "species": "Cat",
            "owner_first_name": "Test",
            "owner_last_name": "Owner"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    patient_id = patient_response.json()["id"]
    
    future_time = (datetime.now() + timedelta(days=1)).isoformat()
    appointment_response = authenticated_client.post(
        "/appointments/",
        json={
            "patient_id": patient_id,
            "appointment_time": future_time,
            "duration_minutes": 30
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    appointment_id = appointment_response.json()["id"]
    
    # Update status to completed
    response = authenticated_client.put(
        f"/appointments/{appointment_id}",
        json={
            "status": "completed"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"

