"""
Database connection and session management

🎯 YOUR MISSION (Week 1-2):
1. Set up SQLAlchemy engine (connects to PostgreSQL)
2. Create a SessionLocal class (manages database sessions)
3. Create a Base class (parent for all models)
4. Create a dependency function to get database sessions

💡 KEY CONCEPTS:
- Engine: The starting point for database connection
- Session: A "workspace" for database operations
- Base: Parent class for all your database models
- Dependency Injection: FastAPI's way of sharing resources
"""

# TODO: Import SQLAlchemy components
# HINT: from sqlalchemy import create_engine
# HINT: from sqlalchemy.ext.declarative import declarative_base
# HINT: from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy import create_engine, URL, text
from sqlalchemy.ext.declarative import declarative_basefrpm 
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import settings



# TODO: Create database engine
# HINT: engine = create_engine(settings.database_url)
# NOTE: The engine manages the connection pool to your database


# TODO: Create SessionLocal class
# HINT: SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# NOTE: This creates a factory for database sessions


# TODO: Create Base class for models
# HINT: Base = declarative_base()
# NOTE: All your models will inherit from this


# TODO: Create a dependency function to get database sessions
# HINT: def get_db():
# HINT:     db = SessionLocal()
# HINT:     try:
# HINT:         yield db  # This provides the session to the endpoint
# HINT:     finally:
# HINT:         db.close()  # Always close when done!


# 📖 UNDERSTANDING THE CODE:
# 
# What's a database session?
# - Think of it like a shopping cart for database operations
# - You add changes to the cart (session.add)
# - Then checkout all at once (session.commit)
# - If something goes wrong, you can cancel (session.rollback)
#
# Why use 'yield' instead of 'return'?
# - 'yield' pauses the function, lets FastAPI use the session, then continues
# - This ensures we always close the session (in the finally block)
#
# What's the purpose of get_db()?
# - FastAPI will call this for every request that needs database access
# - It provides a fresh session and cleans up automatically

# 🧪 TESTING:
# Create a file test_db.py:
# from app.database import SessionLocal
# db = SessionLocal()
# print("Connected!" if db else "Failed")
# db.close()

