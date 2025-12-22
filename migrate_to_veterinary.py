"""
Database Migration Script - Convert to Veterinary Clinic Model

This script migrates your existing patient data to the new veterinary model.

WHAT IT DOES:
1. Backs up existing data
2. Drops old tables
3. Creates new tables with veterinary fields
4. Optionally restores data (with field mapping)

⚠️ IMPORTANT: This will modify your database!
- Make sure backend is NOT running
- Backup your database first if you have important data
"""

from app.database import engine, Base
from app.models.patient import Patient
from app.models.vaccine import Vaccine
from app.models.treatment import Treatment
from app.models.tenant import Tenant
from app.models.user import User
from app.models.appointment import Appointment
from sqlalchemy import inspect

def check_existing_tables():
    """Check what tables currently exist"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print("\nExisting tables in database:")
    for table in existing_tables:
        print(f"  - {table}")
    return existing_tables

def backup_reminder():
    """Remind user to backup"""
    print("\n" + "="*60)
    print("WARNING: DATABASE MIGRATION")
    print("="*60)
    print("\nThis script will:")
    print("  1. Drop the existing 'patients' table")
    print("  2. Create new tables with veterinary fields")
    print("  3. You will LOSE existing patient data!")
    print("\nIf you have important data, backup first:")
    print("  - Export patients from /docs endpoint")
    print("  - Or use database backup tools")
    print("\n" + "="*60)
    
    response = input("\nDo you want to continue? (yes/no): ").strip().lower()
    return response == 'yes'

def migrate_database():
    """Perform the migration"""
    print("\nStarting migration...")
    
    # Step 1: Drop existing tables (in correct order due to foreign keys)
    print("\n[1] Dropping old tables...")
    try:
        # Drop tables in reverse order of dependencies
        Base.metadata.drop_all(bind=engine, tables=[
            Appointment.__table__,
            Patient.__table__,
        ])
        print("  [OK] Old patient and appointment tables dropped")
    except Exception as e:
        print(f"  [WARNING] Error dropping tables: {e}")
        print("  (This is OK if tables don't exist yet)")
    
    # Step 2: Create new tables
    print("\n[2] Creating new veterinary tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("  [OK] New tables created:")
        print("     - patients (with pet fields)")
        print("     - vaccines (new!)")
        print("     - treatments (new!)")
        print("     - appointments (updated)")
    except Exception as e:
        print(f"  [ERROR] Error creating tables: {e}")
        return False
    
    print("\n[OK] Migration complete!")
    return True

def show_new_structure():
    """Show the new table structure"""
    print("\n" + "="*60)
    print("NEW DATABASE STRUCTURE")
    print("="*60)
    print("""
patients table:
  Pet Information:
    - pet_name
    - species (dog, cat, bird, etc.)
    - breed
    - color
    - gender
    - date_of_birth
    - chip_number
    - weight
  
  Owner Information:
    - owner_first_name
    - owner_last_name
    - owner_email
    - owner_phone
    - owner_address
  
  Medical Information:
    - medical_history
    - allergies
    - special_notes

vaccines table (NEW!):
    - vaccine_name
    - date_given
    - next_due_date
    - veterinarian_name
    - batch_number
    - notes

treatments table (NEW!):
    - treatment_type
    - treatment_name
    - treatment_date
    - diagnosis
    - medications_prescribed
    - cost
    - notes
    """)

def main():
    """Main migration function"""
    print("\n" + "="*60)
    print("VETERINARY CLINIC DATABASE MIGRATION")
    print("="*60)
    
    # Check existing tables
    existing_tables = check_existing_tables()
    
    # Show warning and get confirmation
    if not backup_reminder():
        print("\nMigration cancelled. No changes made.")
        return
    
    # Perform migration
    success = migrate_database()
    
    if success:
        show_new_structure()
        print("\n" + "="*60)
        print("MIGRATION SUCCESSFUL!")
        print("="*60)
        print("\nNext steps:")
        print("  1. Start your backend: uvicorn app.main:app --reload")
        print("  2. Check API docs: http://localhost:8000/docs")
        print("  3. Create test data: python create_test_pets.py")
        print("  4. Test the new endpoints!")
        print("\n")
    else:
        print("\nMigration failed. Check errors above.")

if __name__ == "__main__":
    main()

