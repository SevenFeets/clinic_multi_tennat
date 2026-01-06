"""
Tenant Model - Database table for multi-tenancy

 KEY CONCEPTS:
- Tenant = One customer/clinic using your SaaS
- Each tenant's data is isolated from others
- One database, multiple tenants (shared schema approach)
"""

# Import SQLAlchemy components
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
# Import Base
from app.database import Base

# Create Tenant class
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subdomain = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
   
    
    # Define relationships
    users = relationship("User", back_populates="tenant")

    # for Week 4: Add these when you create Patient and Appointment models
    patients = relationship("Patient", back_populates="tenant")
    appointments = relationship("Appointment", back_populates="tenant")
    waitlist_entries = relationship("Waitlist", back_populates="tenant")
    recurring_appointments = relationship("RecurringAppointment", back_populates="tenant")
    
    
    """
    add ons:
    - max_users
    - treatment_plans
    - medical_records
    - medicament history
    - vaccination history
    """

    def __repr__(self):
        return f"<Tenant {self.name} (ID: {self.id})>"
