"""
Patient Management Tests
Tests for patient CRUD operations and multi-tenant isolation
"""
import pytest
from app.models.patient import Patient
from app.models.tenant import Tenant


def test_create_patient(authenticated_client, db_session, test_tenant):
    """Test creating a new patient"""
    response = authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Fluffy",
            "species": "Cat",
            "breed": "Persian",
            "date_of_birth": "2020-01-15",
            "gender": "female",
            "owner_first_name": "John",
            "owner_last_name": "Doe",
            "owner_phone": "123-456-7890",
            "owner_email": "john@example.com"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["pet_name"] == "Fluffy"
    assert data["species"] == "Cat"
    assert "id" in data


def test_get_patients(authenticated_client, db_session, test_tenant):
    """Test retrieving list of patients"""
    # Create a patient first
    authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Buddy",
            "species": "Dog",
            "breed": "Golden Retriever",
            "owner_first_name": "Jane",
            "owner_last_name": "Smith"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    response = authenticated_client.get(
        "/patients/",
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_patient_by_id(authenticated_client, db_session, test_tenant):
    """Test retrieving a specific patient by ID"""
    # Create a patient
    create_response = authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Max",
            "species": "Dog",
            "owner_first_name": "Bob",
            "owner_last_name": "Johnson"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    patient_id = create_response.json()["id"]
    
    # Get the patient
    response = authenticated_client.get(
        f"/patients/{patient_id}",
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == patient_id
    assert data["pet_name"] == "Max"


def test_update_patient(authenticated_client, db_session, test_tenant):
    """Test updating a patient"""
    # Create a patient
    create_response = authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Luna",
            "species": "Cat",
            "owner_first_name": "Alice",
            "owner_last_name": "Brown"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    patient_id = create_response.json()["id"]
    
    # Update the patient
    response = authenticated_client.put(
        f"/patients/{patient_id}",
        json={
            "pet_name": "Luna Updated",
            "species": "Cat",
            "breed": "Siamese",
            "owner_first_name": "Alice",
            "owner_last_name": "Brown"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["pet_name"] == "Luna Updated"
    assert data["breed"] == "Siamese"


def test_delete_patient(authenticated_client, db_session, test_tenant):
    """Test deleting a patient"""
    # Create a patient
    create_response = authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Charlie",
            "species": "Dog",
            "owner_first_name": "David",
            "owner_last_name": "Wilson"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    patient_id = create_response.json()["id"]
    
    # Delete the patient
    response = authenticated_client.delete(
        f"/patients/{patient_id}",
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    
    assert response.status_code == 204
    
    # Verify patient is deleted
    get_response = authenticated_client.get(
        f"/patients/{patient_id}",
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    assert get_response.status_code == 404


def test_multi_tenant_isolation(authenticated_client, db_session, test_tenant):
    """Test that tenants cannot access each other's patients"""
    # Create tenant 2
    tenant2 = Tenant(name="Another Clinic", subdomain="another-clinic")
    db_session.add(tenant2)
    db_session.commit()
    db_session.refresh(tenant2)
    
    # Create patient for tenant 1
    create_response = authenticated_client.post(
        "/patients/",
        json={
            "pet_name": "Isolated Pet",
            "species": "Dog",
            "owner_first_name": "Owner",
            "owner_last_name": "One"
        },
        headers={"X-Tenant-ID": str(test_tenant.id)}
    )
    patient_id = create_response.json()["id"]
    
    # Try to access patient from tenant 2
    response = authenticated_client.get(
        f"/patients/{patient_id}",
        headers={"X-Tenant-ID": str(tenant2.id)}
    )
    
    # Should not find the patient (404 or empty list)
    assert response.status_code in [404, 200]
    if response.status_code == 200:
        # If 200, should be empty or not contain the patient
        data = response.json()
        if isinstance(data, list):
            assert len(data) == 0
        else:
            assert data.get("id") != patient_id

