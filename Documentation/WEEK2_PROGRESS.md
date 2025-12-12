# 📚 Week 2 Progress: Authentication

## ✅ Day 1 Complete: Pydantic Schemas (Nov 4, 2025)

### What You Built Today

Created **5 essential schemas** in `app/schemas/user.py`:

1. **UserBase** - Shared fields (email, full_name)
2. **UserCreate** - For registration (includes password with validation)
3. **UserLogin** - For authentication (email + password)
4. **User** - Response model (NO password! Security first!)
5. **Token** & **TokenData** - For JWT authentication

### Key Concepts You Learned

#### 🔒 **Security Through Schemas**
- ✅ `UserCreate` has password → clients send this
- ✅ `User` has NO password → API returns this
- ❌ **NEVER return passwords to clients!**

#### ✅ **Automatic Validation**
- `EmailStr` → Rejects invalid emails
- `Field(min_length=8)` → Rejects short passwords
- Pydantic does this **automatically** before your code even runs!

#### 🔄 **Schema Inheritance**
- `UserBase` contains shared fields
- `UserCreate` and `User` inherit from it
- DRY principle: Don't Repeat Yourself!

#### 🗃️ **Database Integration**
- `model_config = ConfigDict(from_attributes=True)`
- Allows reading from SQLAlchemy models
- Converts database objects → JSON responses

### What You Tested

```
✅ Valid email + valid password → Accepted
❌ Invalid email format → Rejected automatically
❌ Password < 8 characters → Rejected automatically
✅ Login schema works correctly
```

---

## 📋 Next Steps: Days 2-7

### **Day 2: Password Hashing** 🔒
**File to create:** `app/utils/security.py`

**Functions needed:**
```python
def hash_password(password: str) -> str:
    """Hash a plain password using bcrypt"""
    # Use passlib to hash password
    pass

def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    # Check if password matches hash
    pass

def create_access_token(data: dict) -> str:
    """Create a JWT access token"""
    # Use python-jose to create JWT
    pass

def verify_token(token: str) -> TokenData:
    """Decode and verify a JWT token"""
    # Decode JWT and return user info
    pass
```

**Why this matters:**
- NEVER store plain passwords in database
- bcrypt makes it impossible to reverse the hash
- JWT tokens let users stay logged in

---

### **Day 3: Registration Endpoint** 📝
**File to create:** `app/routers/auth.py`

**Endpoint:** `POST /auth/register`

**What it does:**
1. Accept UserCreate schema
2. Check if email already exists
3. Hash the password
4. Save user to database
5. Return User schema (no password!)

**Test:**
```json
POST /auth/register
{
  "email": "john@example.com",
  "full_name": "John Doe",
  "password": "SecurePass123"
}
```

---

### **Day 4: Login Endpoint** 🔑
**Endpoint:** `POST /auth/login`

**What it does:**
1. Accept UserLogin schema
2. Find user by email
3. Verify password matches hash
4. Generate JWT token
5. Return Token schema

**Test:**
```json
POST /auth/login
{
  "email": "john@example.com",
  "password": "SecurePass123"
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

### **Day 5: Protected Routes** 🛡️
**File to create:** `app/dependencies/auth.py`

**Dependency:** `get_current_user()`

**What it does:**
1. Extract token from request header
2. Decode and verify token
3. Get user from database
4. Return user object

**Endpoint:** `GET /auth/me`

**What it does:**
- Returns current logged-in user info
- Requires valid JWT token

**Test in /docs:**
1. Login to get token
2. Click "Authorize" button
3. Paste token: `Bearer eyJhbGc...`
4. Call `/auth/me` → see your user info!

---

## 🎯 Learning Progress

### Completed ✅
- [x] Database setup (Week 1)
- [x] Pydantic schemas (Day 1)
- [x] Password hashing utilities (Day 2) ⭐ JUST COMPLETED!

### In Progress 🔄
- [ ] Registration endpoint (Day 3) ← YOU ARE HERE
- [ ] Login endpoint (Day 4)
- [ ] Protected routes (Day 5)

### Upcoming 📅
- [ ] Multi-tenancy (Week 3)
- [ ] Patient management (Week 4)
- [ ] Appointments (Week 4)

---

## 💡 Pro Tips for Success

1. **Test Everything in /docs**
   - After each change, visit http://localhost:8000/docs
   - Test your endpoints immediately
   - Fix errors right away

2. **One Function at a Time**
   - Don't try to build everything at once
   - Complete one function, test it, move on
   - Small wins build momentum!

3. **Read Error Messages**
   - Python tells you exactly what's wrong
   - Pydantic shows which field failed validation
   - Don't guess - read the error!

4. **Use Print Statements**
   - Add `print()` to see what's happening
   - Debug step by step
   - Remove prints when done

5. **Commit When Working**
   ```bash
   git add .
   git commit -m "Complete user schemas"
   ```

---

## 📚 Additional Resources

### Pydantic
- [Official Docs](https://docs.pydantic.dev/)
- [Field Validation](https://docs.pydantic.dev/latest/usage/validators/)
- [Examples](https://docs.pydantic.dev/latest/examples/models/)

### FastAPI
- [Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)
- [OAuth2 Tutorial](https://fastapi.tiangolo.com/tutorial/security/)

### JWT
- [What is JWT?](https://jwt.io/introduction)
- [python-jose docs](https://python-jose.readthedocs.io/)

---

## ❓ Common Questions

**Q: Why do we need so many schemas?**
A: Security! Each endpoint needs different data. Registration needs password, but we never return passwords.

**Q: What if I forget to validate something?**
A: Pydantic has your back! If you define it in the schema, it's validated automatically.

**Q: Do I need to memorize all this?**
A: No! This guide is your reference. Come back to it anytime.

**Q: What if something breaks?**
A: That's normal! Read the error, check the docs, try again. You're learning!

---

## 🎉 Celebration Time!

You just learned:
- ✅ How to validate data with Pydantic
- ✅ How to protect sensitive information
- ✅ How to structure API schemas professionally
- ✅ The foundation of authentication systems

**This is huge!** Many developers struggle with these concepts. You're doing great! 💪

---

**Next:** When you're ready, tackle Day 2 - Password Hashing!

Remember: Take breaks, don't rush, and enjoy the process! 🚀

