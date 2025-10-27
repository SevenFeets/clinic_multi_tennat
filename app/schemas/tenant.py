"""
Tenant Schemas - Pydantic models for tenant validation

🎯 YOUR MISSION (Week 3):
Create schemas for tenant operations

💡 HINTS:
- Similar pattern to user schemas
- TenantCreate for creating new tenants
- Tenant for responses
"""

# TODO: Import Pydantic
# HINT: from pydantic import BaseModel, Field
# HINT: from datetime import datetime
# HINT: from typing import Optional


# TODO: Create TenantBase schema
# HINT: class TenantBase(BaseModel):
# HINT:     name: str = Field(..., min_length=1)
# HINT:     subdomain: str = Field(..., min_length=3, max_length=63)


# TODO: Create TenantCreate schema
# HINT: class TenantCreate(TenantBase):
# HINT:     pass  # Inherits all fields from TenantBase


# TODO: Create Tenant schema (response)
# HINT: class Tenant(TenantBase):
# HINT:     id: int
# HINT:     is_active: bool
# HINT:     created_at: datetime
# HINT:     
# HINT:     class Config:
# HINT:         from_attributes = True


# 📖 UNDERSTANDING:
# 
# Subdomain validation:
# - Must be 3-63 characters (DNS standard)
# - Should only contain letters, numbers, hyphens
# - Examples: "clinic1", "dr-smith", "downtown-clinic"
#
# Later you'll add:
# - @validator to check subdomain format
# - Check if subdomain already exists
# - Prevent reserved words ("admin", "api", "www")

# 🎯 CHALLENGE:
# Add a validator to ensure subdomain is lowercase
# and only contains alphanumeric characters and hyphens

