"""
- Each class = one database table
- Each attribute = one database column
- SQLAlchemy handles the SQL for you!
"""
# Import SQLAlchemy components
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime
from datetime import timezone
from app.database import Base


#Create User class that inherits from Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), server_default=func.now())
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    # tenant_id = Column(Integer, ForeignKey("tenants.id")) # For multi-tenancy!

    #  Define relationships (Week 3)
    # tenant = relationship("Tenant", back_populates="users")  # Commented out until Tenant model is created
    last_logins = relationship("LastLogin", back_populates="user")
   


class LastLogin(Base):
    """Table to track user login history"""
    __tablename__ = "last_logins"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    login_time = Column(DateTime, default=lambda: datetime.now(timezone.utc), server_default=func.now(), nullable=False)
    ip_address = Column(String, nullable=True)  # Optional: track where they logged in from
    
    # Relationship back to User
    user = relationship("User", back_populates="last_logins")





# Column Arguments:
# - primary_key=True: Unique identifier for each row
# - unique=True: No two rows can have the same value
# - index=True: Makes searching faster
# - nullable=False: This field is required
# - default=value: Use this value if none provided
#
# Why hash_password and not password?
# - NEVER store plain passwords!
# - We'll hash them in Week 2 with bcrypt
#
# What's ForeignKey?
# - Links to another table (tenant_id links to tenants table)
# - This enables multi-tenant architecture

# 🎯 CHALLENGE:
# Add a last_login field to track when users last logged in
# HINT: Use DateTime column with nullable=True

# 🧪 TESTING (Week 2):
# You'll create users in the database using this model
# For now, just make sure there are no syntax errors!

