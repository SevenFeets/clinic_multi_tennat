from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
import re


class TenantBase(BaseModel):
    """
    Base schema with shared fields for tenant operations.
    
    Fields:
    - name: Full clinic name (e.g., "City Health Clinic")
    - subdomain: URL-friendly identifier (e.g., "cityclinic")
    """
    name: str = Field(..., min_length=1, max_length=100, description="Clinic name")
    subdomain: str = Field(..., min_length=3, max_length=63, description="Unique subdomain identifier")


class TenantCreate(TenantBase):
    """
    Schema for creating new tenants.
    Inherits name and subdomain from TenantBase.
    
    Example:
    {
        "name": "Downtown Wellness Center",
        "subdomain": "downtown"
    }
    """
    
    @field_validator('subdomain')
    @classmethod
    def validate_subdomain(cls, v: str) -> str:
        """
        Validate subdomain format:
        - Must be lowercase
        - Only alphanumeric characters and hyphens
        - Cannot start or end with hyphen
        - No consecutive hyphens
        """
        # Convert to lowercase
        v = v.lower()
        
        # Check format (alphanumeric and hyphens only)
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Subdomain must contain only lowercase letters, numbers, and hyphens')
        
        # Cannot start or end with hyphen
        if v.startswith('-') or v.endswith('-'):
            raise ValueError('Subdomain cannot start or end with a hyphen')
        
        # No consecutive hyphens
        if '--' in v:
            raise ValueError('Subdomain cannot contain consecutive hyphens')
        
        # Reserved words
        reserved = ['admin', 'api', 'www', 'app', 'mail', 'ftp', 'localhost', 'test']
        if v in reserved:
            raise ValueError(f'Subdomain "{v}" is reserved and cannot be used')
        
        return v


class Tenant(TenantBase):
    """
    Schema for returning tenant data (response model).
    Includes all database fields except sensitive information.
    
    Example Response:
    {
        "id": 1,
        "name": "City Health Clinic",
        "subdomain": "cityclinic",
        "is_active": true,
        "created_at": "2025-11-22T13:05:28.932580"
    }
    """
    id: int
    is_active: bool
    created_at: datetime
    
    # Pydantic V2 config - allows reading from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


# 📖 UNDERSTANDING TENANT SCHEMAS:
# 
# Why separate Create and Response schemas?
# - TenantCreate: What clients send (just name and subdomain)
# - Tenant: What API returns (includes id, is_active, created_at)
# - Keeps API clean and secure!
#
# Subdomain validation:
# - Must be 3-63 characters (DNS standard)
# - Lowercase letters, numbers, hyphens only
# - Examples: "clinic1", "dr-smith", "downtown-clinic"
# - Reserved words blocked: "admin", "api", "www", etc.
#
# Real-world usage:
# - cityclinic.yourapp.com → tenant with subdomain "cityclinic"
# - downtown.yourapp.com → tenant with subdomain "downtown"

