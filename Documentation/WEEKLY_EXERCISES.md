# 📚 Weekly Exercises - Learn by Doing!

Each week has hands-on exercises to reinforce what you're learning.

---

## Week 1: Foundation - FastAPI Basics

### Exercise 1: Hello World API
**Goal**: Get comfortable with FastAPI basics

**Tasks**:
1. Create an endpoint at `/hello` that returns `{"message": "Hello World"}`
2. Create an endpoint at `/hello/{name}` that returns `{"message": "Hello {name}"}`
3. Test both in /docs

**Learning**: Path parameters, JSON responses

### Exercise 2: Calculator API
**Goal**: Practice different HTTP methods and request bodies

**Tasks**:
1. Create POST endpoint `/calculate/add` that accepts two numbers and returns their sum
2. Create POST endpoint `/calculate/multiply` for multiplication
3. Use Pydantic schemas to validate input

**Example Input**:
```json
{
  "a": 5,
  "b": 3
}
```

**Example Output**:
```json
{
  "result": 8,
  "operation": "addition"
}
```

**Learning**: POST requests, Pydantic validation, request bodies

### Exercise 3: Database Connection
**Goal**: Connect to PostgreSQL successfully

**Tasks**:
1. Install and start PostgreSQL
2. Create database `clinic_saas`
3. Configure `.env` file
4. Test connection with a simple script
5. Create your first table using SQLAlchemy

**Hint**: Create a simple `test_connection.py`:
```python
from app.database import SessionLocal

db = SessionLocal()
print("Connected!" if db else "Failed")
db.close()
```

**Learning**: PostgreSQL, SQLAlchemy, environment variables

---

## Week 2: Authentication

### Exercise 4: User Registration
**Goal**: Implement secure user registration

**Tasks**:
1. Complete the User model
2. Complete the UserCreate schema
3. Implement password hashing
4. Create registration endpoint
5. Test with /docs

**Test Cases**:
- ✅ Register with valid email and password
- ❌ Register with invalid email format
- ❌ Register with password < 8 characters
- ❌ Register with duplicate email

**Learning**: Password hashing, data validation, database operations

### Exercise 5: Login System
**Goal**: Implement JWT-based authentication

**Tasks**:
1. Implement password verification
2. Create JWT token generation
3. Create login endpoint
4. Test login flow

**Success Criteria**:
- Login returns a token
- Token contains user email
- Token has expiration time

**Learning**: JWT tokens, authentication flow

### Exercise 6: Protected Routes
**Goal**: Secure your API endpoints

**Tasks**:
1. Create `get_current_user` dependency
2. Create a protected endpoint `/auth/me`
3. Test with and without token
4. Add authorization to calculator endpoints

**Test Cases**:
- ✅ Access /auth/me with valid token → returns user info
- ❌ Access /auth/me without token → 401 error
- ❌ Access /auth/me with expired token → 401 error

**Learning**: Dependencies, middleware, JWT verification

---

## Week 3: Multi-Tenancy

### Exercise 7: Tenant Model
**Goal**: Understand multi-tenant architecture

**Tasks**:
1. Complete Tenant model
2. Create TenantCreate schema
3. Add tenant_id to User model
4. Create tenant creation endpoint
5. Manually create 2 test tenants in database

**Tenants to create**:
- Tenant 1: "Clinic A", subdomain: "clinica"
- Tenant 2: "Clinic B", subdomain: "clinicb"

**Learning**: Multi-tenancy concepts, database relationships

### Exercise 8: Tenant Context
**Goal**: Automatically identify tenant per request

**Tasks**:
1. Implement tenant middleware
2. Test with header: `X-Tenant-ID: clinica`
3. Verify tenant is available in request.state
4. Create endpoint that returns current tenant info

**Test**:
```bash
curl -H "X-Tenant-ID: clinica" http://localhost:8000/tenant/info
```

**Learning**: Middleware, request context, headers

### Exercise 9: Data Isolation
**Goal**: Ensure each tenant only sees their data

**Tasks**:
1. Create users for both tenants
2. Create patients for both tenants
3. Verify Tenant A can't see Tenant B's patients
4. Add tenant_id filter to all queries

**Critical Test**:
- Login as Tenant A user
- Try to access Tenant B's patient by ID
- Should get 404, not 403! (Don't reveal patient exists)

**Learning**: Data security, tenant isolation, authorization

---

## Week 4: Core Features

### Exercise 10: Patient CRUD
**Goal**: Build complete patient management

**Tasks**:
1. Complete all patient endpoints
2. Test each CRUD operation:
   - Create 3 patients
   - List all patients
   - Get patient by ID
   - Update patient info
   - Delete patient

**Bonus**: Add search endpoint: `/patients/search?name=John`

**Learning**: CRUD operations, query filtering

### Exercise 11: Appointment Booking
**Goal**: Implement appointment system

**Tasks**:
1. Complete appointment endpoints
2. Create appointment booking logic
3. Add validation (future dates only)
4. Book several test appointments

**Business Logic**:
- Appointments must be in the future
- During business hours (9 AM - 5 PM)
- Duration must be 15, 30, 45, or 60 minutes

**Learning**: DateTime handling, business logic, validation

### Exercise 12: Prevent Double Booking
**Goal**: Add conflict detection

**Tasks**:
1. Write function to check for time conflicts
2. Reject overlapping appointments
3. Test thoroughly:
   - Book appointment at 10:00-10:30
   - Try to book 10:15-10:45 → should fail
   - Book at 10:30-11:00 → should succeed

**Challenge**: Handle edge cases (same start/end time)

**Learning**: Complex queries, business logic, edge cases

---

## Bonus Exercises

### Bonus 1: API Documentation
**Goal**: Make your API professional

**Tasks**:
1. Add descriptions to all endpoints
2. Add examples to schemas
3. Add tags for organization
4. Add response models for errors

**Hint**:
```python
@router.post(
    "/",
    response_model=Patient,
    summary="Create a new patient",
    description="Creates a new patient record for the current tenant.",
    responses={
        201: {"description": "Patient created successfully"},
        400: {"description": "Invalid input"},
        401: {"description": "Not authenticated"}
    }
)
```

### Bonus 2: Error Handling
**Goal**: Handle errors gracefully

**Tasks**:
1. Create custom exception handlers
2. Return consistent error format
3. Add validation errors
4. Log errors properly

**Error Format**:
```json
{
  "error": {
    "code": "PATIENT_NOT_FOUND",
    "message": "Patient with ID 123 not found",
    "details": {}
  }
}
```

### Bonus 3: Basic Tests
**Goal**: Start writing tests

**Tasks**:
1. Set up pytest
2. Write tests for authentication
3. Write tests for patient CRUD
4. Achieve >80% code coverage

**Run tests**: `pytest -v`

---

## Mini-Projects (After Week 4)

### Project 1: Appointment Calendar View
Create an endpoint that returns available time slots for a given date.

**Endpoint**: `GET /appointments/available?date=2024-01-15`

**Returns**:
```json
{
  "date": "2024-01-15",
  "available_slots": [
    "09:00", "09:30", "10:00", "10:30",
    "14:00", "14:30", "15:00"
  ]
}
```

### Project 2: Patient Dashboard
Create an endpoint that returns patient statistics.

**Endpoint**: `GET /dashboard/stats`

**Returns**:
```json
{
  "total_patients": 45,
  "appointments_today": 8,
  "appointments_this_week": 32,
  "new_patients_this_month": 5
}
```

### Project 3: Appointment Reminders
Create a script that sends email reminders for appointments.

**Features**:
- Find appointments in next 24 hours
- Send email to each patient
- Mark as "reminder_sent"

**Hint**: Use Python's `smtplib` or a service like SendGrid

---

## How to Use These Exercises

1. **Read the whole exercise first**: Understand what you're building
2. **Plan your approach**: Think about the steps needed
3. **Write code incrementally**: Test after each small change
4. **Use the hints**: They point you in the right direction
5. **Test thoroughly**: Try to break your own code
6. **Commit when working**: Save your progress!

---

## Grading Yourself

For each exercise:
- ⭐ Basic: Implements core functionality
- ⭐⭐ Good: Handles errors properly
- ⭐⭐⭐ Great: Includes validation and tests
- ⭐⭐⭐⭐ Excellent: Production-ready code

**Don't aim for 4 stars right away!** Start with 1 star and improve iteratively.

---

## Need Help?

**Stuck on an exercise?**
1. Re-read the learning resources in README.md
2. Check the HINTS in the template files
3. Break it into smaller steps
4. Google specific issues
5. Skip and come back later (it's okay!)

**Remember**: These exercises are here to help you learn, not to frustrate you. Take your time and enjoy the process! 🚀

