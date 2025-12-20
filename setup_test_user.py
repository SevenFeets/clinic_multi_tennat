"""
Setup Test User for Authentication Testing

This script creates:
1. A test tenant (cityclinic)
2. A test user (doctor@cityclinic.com)

Run this before testing authentication!
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.tenant import Tenant
from app.models.user import User
from app.utils.security import hash_password
import app.models.tenant  # Import to create tables
import app.models.user  # Import to create tables


def setup_test_data():
    """Create test tenant and user"""
    
    # Create database tables
    print("[*] Creating database tables...")
    from app.models.tenant import Base as TenantBase
    from app.models.user import Base as UserBase
    TenantBase.metadata.create_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)
    print("[+] Tables created!")
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # 1. Check if tenant exists
        print("\n[*] Setting up tenant...")
        tenant = db.query(Tenant).filter(Tenant.subdomain == "cityclinic").first()
        
        if not tenant:
            # Create tenant
            tenant = Tenant(
                name="City Clinic",
                subdomain="cityclinic",
                is_active=True
            )
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
            print(f"[+] Created tenant: {tenant.name} (ID: {tenant.id})")
        else:
            print(f"[+] Tenant already exists: {tenant.name} (ID: {tenant.id})")
        
        # 2. Check if user exists
        print("\n[*] Setting up test user...")
        test_email = "doctor@cityclinic.com"
        user = db.query(User).filter(User.email == test_email).first()
        
        if not user:
            # Create user
            user = User(
                email=test_email,
                full_name="Dr. John Smith",
                hashed_password=hash_password("password123"),
                is_active=True,
                tenant_id=tenant.id
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"[+] Created user: {user.email}")
            print(f"    Name: {user.full_name}")
            print(f"    Password: password123")
            print(f"    Tenant: {tenant.name}")
        else:
            print(f"[+] User already exists: {user.email}")
            print(f"    Name: {user.full_name}")
            print(f"    Tenant: {tenant.name}")
        
        print("\n" + "="*60)
        print("SUCCESS! Test credentials:")
        print("="*60)
        print(f"Email:    {test_email}")
        print(f"Password: password123")
        print(f"Tenant:   {tenant.subdomain}")
        print("="*60)
        print("\nYou can now test login at: http://localhost:5173")
        
    except Exception as e:
        print(f"[-] Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting test data setup...\n")
    setup_test_data()

