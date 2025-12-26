# 📖 Developer Cheat Sheet

Quick reference for common tasks and concepts.

---

## 🐍 Python Basics You'll Need

### Type Hints
```python
# Variables
name: str = "John"
age: int = 25
price: float = 19.99
is_active: bool = True

# Functions
def greet(name: str) -> str:
    return f"Hello {name}"

# Optional types
from typing import Optional
email: Optional[str] = None  # Can be string or None

# Lists
from typing import List
names: List[str] = ["Alice", "Bob"]
```

### Async/Await
```python
# Regular function
def get_data():
    return "data"

# Async function (used in FastAPI)
async def get_data():
    return "data"

# Both work the same for simple cases
# Async is needed for database operations
```

### Dictionaries
```python
# Create
user = {"name": "John", "age": 25}

# Access
print(user["name"])  # John
print(user.get("email", "no email"))  # no email

# Unpack
user_data = {"email": "test@test.com", "name": "John"}
new_user = User(**user_data)  # Same as User(email="...", name="...")
```

---

## 🚀 Terminal Commands

### Virtual Environment
```bash
# Create
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Deactivate
deactivate

# You know it's active when you see (venv) in prompt
```

### Package Management
```bash
# Install from requirements.txt
pip install -r requirements.txt

# Install single package
pip install fastapi

# Update pip
python -m pip install --upgrade pip

# See installed packages
pip list

# Save current packages to requirements.txt
pip freeze > requirements.txt
```

### Running the Server
```bash
# Development mode (auto-reload)
uvicorn app.main:app --reload

# Different port
uvicorn app.main:app --reload --port 8001

# Production mode (no reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Testing
```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_auth.py

# Verbose output
pytest -v

# With coverage
pytest --cov

# Stop on first failure
pytest -x
```

---

## 🗄️ PostgreSQL Commands

### psql Commands
```sql
-- Connect to PostgreSQL
psql -U postgres

-- List databases
\l

-- Connect to database
\c clinic_saas

-- List tables
\dt

-- Describe table
\d users

-- Quit
\q
```

### SQL Basics
```sql
-- Create database
CREATE DATABASE clinic_saas;

-- Create user
CREATE USER clinic_user WITH PASSWORD 'password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE clinic_saas TO clinic_user;

-- View data
SELECT * FROM users;
SELECT * FROM users WHERE email = 'test@test.com';

-- Count records
SELECT COUNT(*) FROM patients;

-- Delete all data (careful!)
TRUNCATE TABLE users CASCADE;
```

---

## 🎯 FastAPI Patterns

### Basic Endpoint
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Path Parameters
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}
```

### Query Parameters
```python
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Call: /items?skip=20&limit=5
```

### Request Body
```python
from pydantic import BaseModel

class User(BaseModel):
    email: str
    name: str

@app.post("/users")
async def create_user(user: User):
    return user
```

### Dependencies
```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
async def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

### Headers
```python
from fastapi import Header

@app.get("/items")
async def read_items(x_token: str = Header(None)):
    return {"token": x_token}
```

---

## 🔐 Authentication Patterns

### Hash Password
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

# Hash
hashed = pwd_context.hash("mypassword")

# Verify
is_valid = pwd_context.verify("mypassword", hashed)
```

### Create JWT Token
```python
from jose import jwt
from datetime import datetime, timedelta

data = {"sub": "user@example.com"}
expire = datetime.utcnow() + timedelta(minutes=30)
data.update({"exp": expire})

token = jwt.encode(data, SECRET_KEY, algorithm="HS256")
```

### Verify JWT Token
```python
from jose import jwt, JWTError

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    email = payload.get("sub")
except JWTError:
    # Invalid token
    pass
```

### Protected Endpoint
```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify token and return user
    pass

@app.get("/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {"user": current_user}
```

---

## 🗃️ SQLAlchemy Patterns

### Define Model
```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
```

### Create Record
```python
new_user = User(email="test@test.com", name="Test")
db.add(new_user)
db.commit()
db.refresh(new_user)  # Get generated ID
```

### Read Records
```python
# Get all
users = db.query(User).all()

# Get one
user = db.query(User).filter(User.email == "test@test.com").first()

# Get by ID
user = db.query(User).filter(User.id == 1).first()

# With limit and offset
users = db.query(User).offset(10).limit(20).all()
```

### Update Record
```python
user = db.query(User).filter(User.id == 1).first()
user.name = "New Name"
db.commit()
```

### Delete Record
```python
user = db.query(User).filter(User.id == 1).first()
db.delete(user)
db.commit()
```

### Relationships
```python
# One-to-Many
class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True)
    users = relationship("User", back_populates="tenant")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    tenant = relationship("Tenant", back_populates="users")

# Access
tenant = db.query(Tenant).first()
print(tenant.users)  # List of users for this tenant

user = db.query(User).first()
print(user.tenant)  # The tenant object
```

---

## 🧪 Testing Patterns

### Basic Test
```python
def test_something():
    result = 2 + 2
    assert result == 4
```

### Test API Endpoint
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### Test with Authentication
```python
def test_protected_endpoint():
    # Login
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "password"
    })
    token = response.json()["access_token"]
    
    # Use token
    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

---

## 📊 Pydantic Patterns

### Basic Schema
```python
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True  # Allows reading from ORM models
```

### Validation
```python
from pydantic import BaseModel, EmailStr, Field, validator

class User(BaseModel):
    email: EmailStr  # Validates email format
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def password_must_be_strong(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain a number')
        return v
```

---

## 🔍 Debugging Tips

### Print Debugging
```python
# See what's in a variable
print(f"User: {user}")
print(f"Type: {type(user)}")

# Pretty print dictionaries
from pprint import pprint
pprint(user.__dict__)
```

### Check FastAPI Errors
```python
# FastAPI shows detailed errors in browser
# Check terminal for stack traces
# Look for line numbers in your code
```

### Database Debugging
```python
# See the SQL being executed
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    print(f"SQL: {statement}")
```

---

## 🎨 HTTP Status Codes

```python
from fastapi import status

# Success
200  # OK - Standard success
201  # Created - New resource created
204  # No Content - Success but no data to return

# Client Errors
400  # Bad Request - Invalid input
401  # Unauthorized - Not authenticated
403  # Forbidden - Authenticated but not allowed
404  # Not Found - Resource doesn't exist
422  # Unprocessable Entity - Validation failed

# Server Errors
500  # Internal Server Error - Something went wrong
```

---

## 📚 Quick References

### URLs to Remember
- Your API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Important Files
- `app/main.py` - Entry point
- `app/database.py` - Database connection
- `app/config.py` - Settings
- `.env` - Environment variables (NEVER commit!)
- `requirements.txt` - Dependencies

### Common Errors

**"ModuleNotFoundError"**
→ Virtual environment not activated or package not installed

**"Port already in use"**
→ Another process using port 8000
→ Solution: `uvicorn app.main:app --reload --port 8001`

**"Database connection failed"**
→ PostgreSQL not running or wrong credentials in .env

**"422 Unprocessable Entity"**
→ Request body doesn't match schema
→ Check /docs for expected format

---

## 💡 Pro Tips

1. **Use /docs constantly** - Test as you code
2. **Keep the server running** - `--reload` auto-restarts
3. **Read error messages** - They tell you exactly what's wrong
4. **Commit working code** - Save your progress
5. **Google is your friend** - "FastAPI [your question]"
6. **Type hints help** - Your IDE can autocomplete better
7. **Test edge cases** - What if the input is empty? Negative? Huge?

---

## 🆘 When Stuck

1. Read the error message carefully
2. Check the HINTS in template files
3. Google the exact error message
4. Check FastAPI docs
5. Try a simpler version first
6. Take a break and come back

**Remember**: Everyone gets stuck. It's part of learning! 🚀

--- 

# adding source to path example

[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\lnrmy\AppData\Roaming\Python\Python311\Scripts", 
[EnvironmentVariableTarget]::User)

# and check 

$env:PATH -split ';' | Select-String "AppData\\Roaming\\Python"

---

# Alembic: 
python -m alembic init alembic