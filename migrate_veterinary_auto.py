"""
Automatic Database Migration Script - Convert to Veterinary Clinic Model
(Non-interactive version - automatically runs migration)
"""

from app.database import engine, Base
from app.models.patient import Patient
from app.models.vaccine import Vaccine
from app.models.treatment import Treatment
from app.models.tenant import Tenant
from app.models.user import User
from app.models.appointment import Appointment
from sqlalchemy import inspect

def migrate_database():
    """Perform the migration automatically"""
    print("\n" + "="*60)
    print("AUTOMATIC VETERINARY CLINIC DATABASE MIGRATION")
    print("="*60)
    
    # Check existing tables
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print("\nExisting tables:")
    for table in existing_tables:
        print(f"  - {table}")
    
    print("\n" + "="*60)
    print("WARNING: This will drop 'patients' and 'appointments' tables")
    print("="*60)
    
    # Step 1: Drop existing tables
    print("\n[1] Dropping old tables...")
    try:
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
        print("     - vaccines (NEW!)")
        print("     - treatments (NEW!)")
        print("     - appointments (updated)")
    except Exception as e:
        print(f"  [ERROR] Error creating tables: {e}")
        return False
    
    print("\n[OK] Migration complete!")
    return True

def main():
    """Main function"""
    success = migrate_database()
    
    if success:
        print("\n" + "="*60)
        print("MIGRATION SUCCESSFUL!")
        print("="*60)
        print("\nNew database structure:")
        print("  patients - Pet information + Owner information")
        print("  vaccines - Vaccination history")
        print("  treatments - Treatment records")
        print("\nNext steps:")
        print("  1. Run: python create_test_pets.py")
        print("  2. Start backend: uvicorn app.main:app --reload")
        print("  3. Check API: http://localhost:8000/docs")
        print()
    else:
        print("\n[ERROR] Migration failed. Check errors above.")

if __name__ == "__main__":
    main()

