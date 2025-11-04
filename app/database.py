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
from sqlalchemy.orm import sessionmaker, declarative_base

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


