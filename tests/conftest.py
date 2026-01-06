"""
Pytest Configuration and Fixtures
Shared test setup for all test files
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models.user import User
from app.models.tenant import Tenant
from app.utils.security import get_password_hash


# Test database (in-memory SQLite for speed)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_tenant(db_session):
    """Create a test tenant"""
    tenant = Tenant(
        name="Test Clinic",
        subdomain="test-clinic"
    )
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)
    return tenant


@pytest.fixture(scope="function")
def test_user(db_session, test_tenant):
    """Create a test user"""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User",
        tenant_id=test_tenant.id,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def authenticated_client(client, test_user):
    """Create an authenticated test client"""
    # Login to get token
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "testpassword123"
        }
    )
    token = response.json()["access_token"]
    
    # Set authorization header
    client.headers = {"Authorization": f"Bearer {token}"}
    return client

