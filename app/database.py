"""
Database connection and session management

🎯 MISSION COMPLETED (Week 1-2):
1. ✅ Set up SQLAlchemy engine (connects to PostgreSQL)
2. ✅ Create a SessionLocal class (manages database sessions)
3. ✅ Create a Base class (parent for all models)
4. ✅ Create a dependency function to get database sessions

💡 KEY CONCEPTS:
- Engine: The starting point for database connection
- Session: A "workspace" for database operations
- Base: Parent class for all your database models
- Dependency Injection: FastAPI's way of sharing resources
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


# Create database engine (connects to PostgreSQL)
engine = create_engine(
    settings.database_url,
    echo=True,  # Shows SQL queries in console (helpful for learning!)
    pool_pre_ping=True,  # Checks connection health before using
)

# Create SessionLocal class (session factory)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base class for models
# All your database models will inherit from this
Base = declarative_base()


# Dependency function to get database sessions
def get_db():
    """
    FastAPI dependency that provides a database session.
    Automatically closes the session after the request.
    
    Usage in endpoints:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db  # Provide session to the endpoint
    except Exception as e:
        db.rollback()  # Rollback on error
        raise e
    finally:
        db.close()  # Always close the session


# 🧪 TESTING:
# Create a file test_db_connection.py in project root:
#
# from app.database import SessionLocal
# from sqlalchemy import text
#
# print("Testing database connection...")
# try:
#     db = SessionLocal()
#     result = db.execute(text("SELECT current_database()"))
#     db_name = result.scalar()
#     print(f"✅ Connected to database: {db_name}")
#     db.close()
# except Exception as e:
#     print(f"❌ Connection failed: {e}")
