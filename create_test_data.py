"""
Create Test Data for Dashboard
Creates sample patients and appointments to demonstrate real-time stats
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.patient import Patient
from app.models.appointment import Appointment, AppointmentStatus
from app.models.tenant import Tenant
import random


def create_test_data():
    """Create test patients and appointments"""
    db: Session = SessionLocal()
    
    try:
        # Get the cityclinic tenant
        tenant = db.query(Tenant).filter(Tenant.subdomain == "cityclinic").first()
        if not tenant:
            print("[-] Error: Tenant 'cityclinic' not found. Run setup_test_user.py first!")
            return
        
        print(f"[*] Using tenant: {tenant.name} (ID: {tenant.id})")
        
        # Check if test data already exists
        existing_patients = db.query(Patient).filter(Patient.tenant_id == tenant.id).count()
        if existing_patients > 5:
            print(f"[!] Test data already exists ({existing_patients} patients)")
            print("[!] Skipping creation to avoid duplicates")
            return
        
        print("\n[*] Creating test patients...")
        
        # Sample pet data
        pet_names = [
            ("Max", "Dog", "Golden Retriever"),
            ("Luna", "Cat", "Persian"),
            ("Charlie", "Dog", "Labrador"),
            ("Bella", "Cat", "Siamese"),
            ("Cooper", "Dog", "German Shepherd"),
            ("Milo", "Cat", "Maine Coon"),
            ("Buddy", "Dog", "Beagle"),
            ("Daisy", "Cat", "Bengal"),
            ("Rocky", "Dog", "Bulldog"),
            ("Chloe", "Cat", "Ragdoll"),
            ("Zeus", "Dog", "Husky"),
            ("Willow", "Cat", "British Shorthair")
        ]
        
        owner_contacts = [
            ("john.smith@email.com", "555-0101", "123 Oak St"),
            ("sarah.johnson@email.com", "555-0102", "456 Pine Ave"),
            ("mike.williams@email.com", "555-0103", "789 Maple Dr"),
            ("emily.brown@email.com", "555-0104", "321 Elm St"),
            ("david.jones@email.com", "555-0105", "654 Cedar Ln"),
            ("lisa.garcia@email.com", "555-0106", "987 Birch Rd"),
        ]
        
        patients = []
        for i, (pet_name, species, breed) in enumerate(pet_names):
            owner_email, phone, address = owner_contacts[i % len(owner_contacts)]
            
            # Generate birth date (1-10 years ago)
            years_ago = random.randint(1, 10)
            dob = datetime.now() - timedelta(days=years_ago * 365)
            
            patient = Patient(
                first_name=pet_name,
                last_name=f"({breed})",
                email=owner_email,
                phone=phone,
                date_of_birth=dob.date(),
                address=address,
                medical_history=f"{species} - {breed}. Regular checkups, vaccinations up to date.",
                tenant_id=tenant.id
            )
            db.add(patient)
            patients.append(patient)
        
        db.commit()
        print(f"[+] Created {len(patients)} patients")
        
        # Refresh to get IDs
        for p in patients:
            db.refresh(p)
        
        print("\n[*] Creating test appointments...")
        
        # Create appointments at various times
        now = datetime.now()
        today_start = datetime(now.year, now.month, now.day, 9, 0, 0)
        
        appointment_data = [
            # Today's appointments
            (today_start + timedelta(hours=0), 30, AppointmentStatus.completed, "Routine checkup"),
            (today_start + timedelta(hours=1), 45, AppointmentStatus.completed, "Vaccination"),
            (today_start + timedelta(hours=2), 30, AppointmentStatus.completed, "Dental cleaning"),
            (today_start + timedelta(hours=3), 60, AppointmentStatus.scheduled, "Surgery consultation"),
            (today_start + timedelta(hours=4), 30, AppointmentStatus.scheduled, "Follow-up visit"),
            (today_start + timedelta(hours=5), 45, AppointmentStatus.scheduled, "Blood test"),
            (today_start + timedelta(hours=6), 30, AppointmentStatus.scheduled, "Grooming"),
            (today_start + timedelta(hours=7), 30, AppointmentStatus.scheduled, "X-ray"),
            
            # Tomorrow
            (today_start + timedelta(days=1, hours=1), 30, AppointmentStatus.scheduled, "Checkup"),
            (today_start + timedelta(days=1, hours=3), 45, AppointmentStatus.scheduled, "Vaccination"),
            (today_start + timedelta(days=1, hours=5), 30, AppointmentStatus.scheduled, "Consultation"),
            
            # Next week
            (today_start + timedelta(days=3, hours=2), 60, AppointmentStatus.scheduled, "Surgery"),
            (today_start + timedelta(days=4, hours=3), 30, AppointmentStatus.scheduled, "Follow-up"),
            (today_start + timedelta(days=5, hours=4), 45, AppointmentStatus.scheduled, "Checkup"),
            (today_start + timedelta(days=6, hours=2), 30, AppointmentStatus.scheduled, "Vaccination"),
        ]
        
        for i, (appt_time, duration, status, note_text) in enumerate(appointment_data):
            patient = patients[i % len(patients)]
            
            appointment = Appointment(
                patient_id=patient.id,
                tenant_id=tenant.id,
                appointment_time=appt_time,
                duration_minutes=duration,
                status=status,
                notes=f"{note_text} for {patient.first_name}"
            )
            db.add(appointment)
        
        db.commit()
        print(f"[+] Created {len(appointment_data)} appointments")
        
        # Calculate and show stats
        total_patients = len(patients)
        today_appointments = sum(1 for a in appointment_data if a[0].date() == now.date())
        completed_today = sum(1 for a in appointment_data if a[0].date() == now.date() and a[2] == AppointmentStatus.completed)
        pending = sum(1 for a in appointment_data if a[2] == AppointmentStatus.scheduled)
        
        print("\n" + "="*60)
        print("SUCCESS! Test data created:")
        print("="*60)
        print(f"Total Patients:        {total_patients}")
        print(f"Today's Appointments:  {today_appointments}")
        print(f"Completed Today:       {completed_today}")
        print(f"Pending Appointments:  {pending}")
        print(f"Estimated Revenue:     ${completed_today * 50}")
        print("="*60)
        print("\n[+] Refresh your dashboard to see the real data!")
        
    except Exception as e:
        print(f"[-] Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Creating test data for dashboard...\n")
    create_test_data()

