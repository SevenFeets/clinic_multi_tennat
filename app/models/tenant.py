"""
Tenant Model - Database table for multi-tenancy

🎯 YOUR MISSION (Week 3):
Create a Tenant model for multi-tenant architecture

📚 LEARNING RESOURCES:
- Multi-Tenancy Patterns: https://docs.microsoft.com/en-us/azure/architecture/guide/multitenant/overview
- What is Multi-Tenancy?: https://www.youtube.com/watch?v=VGXqBHwkXQo

💡 KEY CONCEPTS:
- Tenant = One customer/clinic using your SaaS
- Each tenant's data is isolated from others
- One database, multiple tenants (shared schema approach)
"""

# TODO: Import SQLAlchemy components
# HINT: from sqlalchemy import Column, Integer, String, Boolean, DateTime
# HINT: from sqlalchemy.orm import relationship
# HINT: from datetime import datetime

# TODO: Import Base
# HINT: from app.database import Base


# TODO: Create Tenant class
# HINT: class Tenant(Base):

    # TODO: Set table name
    # HINT: __tablename__ = "tenants"
    
    # TODO: Define columns
    # HINT: id = Column(Integer, primary_key=True, index=True)
    # HINT: name = Column(String, nullable=False)  # Clinic name
    # HINT: subdomain = Column(String, unique=True, nullable=False)  # e.g., "clinic1"
    # HINT: is_active = Column(Boolean, default=True)
    # HINT: created_at = Column(DateTime, default=datetime.utcnow)
    
    # TODO: Define relationships
    # HINT: users = relationship("User", back_populates="tenant")
    # HINT: patients = relationship("Patient", back_populates="tenant")
    # HINT: appointments = relationship("Appointment", back_populates="tenant")


# 📖 UNDERSTANDING MULTI-TENANCY:
# 
# What problem does this solve?
# - Without multi-tenancy: You'd need separate database for each clinic
# - With multi-tenancy: One database serves all clinics, data is isolated
#
# How does subdomain work?
# - clinic1.yourapp.com → tenant_id = 1
# - clinic2.yourapp.com → tenant_id = 2
# - Each tenant only sees their own data
#
# Real-world example:
# - Shopify: Each store is a tenant
# - Slack: Each workspace is a tenant
# - Your app: Each clinic is a tenant!

# 🎯 CHALLENGE:
# Add fields for:
# - max_users (limit how many users per tenant)
# - subscription_tier (basic, premium, enterprise)
# - subscription_expires_at (DateTime)

# 🧪 TESTING (Week 3):
# You'll create tenants and test data isolation

