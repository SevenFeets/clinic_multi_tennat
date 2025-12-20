"""
Create Test Appointments Only
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.patient import Patient
from app.models.appointment import Appointment, AppointmentStatus
from app.models.tenant import Tenant


def create_appointments():
    """Create test appointments"""
    db: Session = SessionLocal()
    
    try:
        # Get the cityclinic tenant
        tenant = db.query(Tenant).filter(Tenant.subdomain == "cityclinic").first()
        if not tenant:
            print("[-] Error: Tenant 'cityclinic' not found!")
            return
        
        print(f"[*] Using tenant: {tenant.name}")
        
        # Get patients
        patients = db.query(Patient).filter(Patient.tenant_id == tenant.id).all()
        if not patients:
            print("[-] No patients found! Run create_test_data.py first!")
            return
        
        print(f"[*] Found {len(patients)} patients")
        
        # Clear existing appointments to avoid duplicates
        existing = db.query(Appointment).filter(Appointment.tenant_id == tenant.id).delete()
        print(f"[*] Cleared {existing} existing appointments")
        
        print("\n[*] Creating appointments...")
        
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
        print("SUCCESS! Your dashboard will show:")
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
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Creating test appointments...\n")
    create_appointments()

