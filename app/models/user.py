"""
User Model - Database table for users

🎯 YOUR MISSION (Week 2):
Create a User model with proper fields and relationships

📚 LEARNING RESOURCES:
- SQLAlchemy Models: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html
- Column Types: https://docs.sqlalchemy.org/en/20/core/types.html

💡 KEY CONCEPTS:
- Each class = one database table
- Each attribute = one database column
- SQLAlchemy handles the SQL for you!
"""

# TODO: Import SQLAlchemy components
# HINT: from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
# HINT: from sqlalchemy.orm import relationship
# HINT: from datetime import datetime

# TODO: Import Base from database.py
# HINT: from app.database import Base


# TODO: Create User class that inherits from Base
# HINT: class User(Base):

    # TODO: Set table name
    # HINT: __tablename__ = "users"
    
    # TODO: Define columns
    # HINT: id = Column(Integer, primary_key=True, index=True)
    # HINT: email = Column(String, unique=True, index=True, nullable=False)
    # HINT: hashed_password = Column(String, nullable=False)
    # HINT: full_name = Column(String)
    # HINT: is_active = Column(Boolean, default=True)
    # HINT: is_superuser = Column(Boolean, default=False)
    # HINT: created_at = Column(DateTime, default=datetime.utcnow)
    # HINT: tenant_id = Column(Integer, ForeignKey("tenants.id"))  # For multi-tenancy!
    
    # TODO: Define relationships (Week 3)
    # HINT: tenant = relationship("Tenant", back_populates="users")


# 📖 UNDERSTANDING THE CODE:
# 
# Column Types:
# - Integer: Whole numbers (1, 2, 3...)
# - String: Text (email, name, etc.)
# - Boolean: True/False
# - DateTime: Date and time stamps
#
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

