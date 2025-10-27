"""
Authentication Tests

🎯 YOUR MISSION (Week 4):
Write tests for your authentication endpoints

📚 LEARNING RESOURCES:
- Pytest Tutorial: https://docs.pytest.org/en/stable/getting-started.html
- Testing FastAPI: https://fastapi.tiangolo.com/tutorial/testing/

💡 KEY CONCEPTS:
- Automated tests catch bugs early
- Test happy path AND error cases
- Use test database (don't mess with real data!)
- Tests document how your API works
"""

# TODO: Import testing tools
# HINT: import pytest
# HINT: from fastapi.testclient import TestClient
# HINT: from app.main import app
# HINT: from app.database import Base, engine

# TODO: Create test client
# HINT: client = TestClient(app)


# TODO: Setup and teardown (create/drop test tables)
# HINT: @pytest.fixture(scope="module")
# HINT: def setup_database():
# HINT:     Base.metadata.create_all(bind=engine)
# HINT:     yield
# HINT:     Base.metadata.drop_all(bind=engine)


# TODO: Test user registration
# HINT: def test_register_user(setup_database):
# HINT:     response = client.post(
# HINT:         "/auth/register",
# HINT:         json={
# HINT:             "email": "test@example.com",
# HINT:             "password": "testpassword123",
# HINT:             "full_name": "Test User"
# HINT:         }
# HINT:     )
# HINT:     assert response.status_code == 201
# HINT:     assert response.json()["email"] == "test@example.com"
# HINT:     assert "password" not in response.json()  # Important!


# TODO: Test duplicate email registration
# HINT: def test_register_duplicate_email(setup_database):
# HINT:     # Try to register same email twice
# HINT:     # Second attempt should fail with 400
# HINT:     pass


# TODO: Test login
# HINT: def test_login(setup_database):
# HINT:     response = client.post(
# HINT:         "/auth/login",
# HINT:         data={
# HINT:             "username": "test@example.com",
# HINT:             "password": "testpassword123"
# HINT:         }
# HINT:     )
# HINT:     assert response.status_code == 200
# HINT:     assert "access_token" in response.json()
# HINT:     assert response.json()["token_type"] == "bearer"


# TODO: Test login with wrong password
# HINT: def test_login_wrong_password(setup_database):
# HINT:     # Should return 401 Unauthorized
# HINT:     pass


# TODO: Test protected endpoint
# HINT: def test_get_current_user(setup_database):
# HINT:     # First login to get token
# HINT:     # Then access /auth/me with token
# HINT:     # Should return user info
# HINT:     pass


# TODO: Test protected endpoint without token
# HINT: def test_protected_without_token():
# HINT:     response = client.get("/auth/me")
# HINT:     assert response.status_code == 401


# 📖 UNDERSTANDING TESTING:
# 
# Test Structure (AAA Pattern):
# - Arrange: Set up test data
# - Act: Execute the code
# - Assert: Check the results
#
# Why Test?
# - Catch bugs before users do
# - Safe refactoring (tests catch breaks)
# - Documentation of expected behavior
# - Confidence in your code
#
# What to Test:
# ✅ Happy path (everything works)
# ✅ Error cases (invalid input)
# ✅ Edge cases (empty strings, null values)
# ✅ Security (unauthorized access)

# 🎯 CHALLENGE:
# Write tests for:
# - Patient CRUD operations
# - Appointment booking
# - Multi-tenant isolation
# - Input validation

# 🧪 RUNNING TESTS:
# pytest
# pytest tests/test_auth.py
# pytest -v  # verbose output
# pytest --cov  # with coverage report

# 💡 TIP:
# Use fixtures for common setup:
# - @pytest.fixture for test database
# - @pytest.fixture for authenticated client
# - @pytest.fixture for sample data

