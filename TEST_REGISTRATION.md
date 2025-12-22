# 🔍 Registration Debug Test

## ✅ New Fixes Applied

1. **Better JSON parsing** - Catches parse errors
2. **Multiple error format checks** - Checks detail, message, error fields
3. **Force string conversion** - Uses `String()` to ensure string output
4. **Enhanced logging** - See full error object in console

---

## 🧪 CRITICAL TEST - Do This Step by Step:

### **Step 1: Check Backend is Running**

Open: http://localhost:8000/docs

✅ **Should see:** FastAPI documentation page  
❌ **If not:** Start backend: `uvicorn app.main:app --reload`

---

### **Step 2: Test Backend Directly**

In http://localhost:8000/docs:

1. Find **POST /auth/register**
2. Click **"Try it out"**
3. Enter this JSON:

```json
{
  "email": "backend-test@clinic.com",
  "password": "testpass123",
  "full_name": "Backend Test User",
  "tenant_id": 1
}
```

4. Click **Execute**

**Expected Response (201 Created):**
```json
{
  "id": 6,
  "email": "backend-test@clinic.com",
  "full_name": "Backend Test User",
  "tenant_id": 1,
  "is_active": true
}
```

✅ **If this works** → Backend is fine!  
❌ **If this fails** → Backend has an issue

---

### **Step 3: Test Frontend Registration**

1. Open: http://localhost:5173/register

2. **OPEN BROWSER CONSOLE (F12) - CRITICAL!**

3. Fill in the form:
```
Full Name: Frontend Test User
Email: frontend-test@clinic.com
Password: TestPass123
Confirm Password: TestPass123
```

**IMPORTANT:** Password MUST contain:
- At least 8 characters
- One uppercase letter (T, P)
- One lowercase letter (e, s, t, a, s)
- One number (1, 2, 3)

4. Click **"Create Account"**

5. **CHECK THE CONSOLE** - You should see:
```
Registration error: [the error]
Error type: [string or object]
Error object: [full object details]
Final error message (string): [the message]
```

---

## 📋 **Copy and Send Me:**

### **Console Output:**
```
[Paste everything from console here]
```

### **Network Tab:**
1. Open F12 → Network tab
2. Try to register
3. Look for the request to `/auth/register`
4. Click on it
5. Check the **Response** tab

**What does it say?**
```
[Paste response here]
```

---

## 🎯 Common Issues & Solutions:

### **Issue 1: CORS Error**
**Console shows:** "CORS policy" or "Access-Control-Allow-Origin"  
**Fix:** Backend CORS not configured  
**Solution:** Check backend allows http://localhost:5173

### **Issue 2: Network Error**
**Console shows:** "Failed to fetch" or "Network request failed"  
**Fix:** Backend not running or wrong URL  
**Solution:** Check backend is at http://localhost:8000

### **Issue 3: 404 Not Found**
**Console shows:** 404 status  
**Fix:** Wrong endpoint  
**Solution:** Check URL is correct

### **Issue 4: 400 Bad Request**
**Console shows:** 400 status  
**Response says:** "Email already registered" or validation error  
**Fix:** Use different email or fix validation  

### **Issue 5: 422 Unprocessable Entity**
**Console shows:** 422 status  
**Fix:** Data format wrong  
**Solution:** Check tenant_id is a number (1)

---

## 🔧 Emergency Diagnostic Script

Open browser console and run:

```javascript
// Test 1: Check if API is reachable
fetch('http://localhost:8000/docs')
  .then(r => console.log('✅ Backend reachable:', r.status))
  .catch(e => console.log('❌ Backend NOT reachable:', e));

// Test 2: Try registration directly
fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Tenant-ID': 'cityclinic'
  },
  body: JSON.stringify({
    email: 'console-test@clinic.com',
    password: 'testpass123',
    full_name: 'Console Test',
    tenant_id: 1
  })
})
  .then(r => r.json())
  .then(data => console.log('✅ Registration response:', data))
  .catch(e => console.log('❌ Registration failed:', e));
```

**Run this in console and tell me what you see!**

---

## 📸 Send Me Screenshots Of:

1. **The error message** on the page
2. **The browser console** (F12 → Console)
3. **The network request** (F12 → Network → click on /auth/register)
4. **The backend terminal** (where uvicorn is running)

---

## ⚡ Quick Checklist:

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Browser console open (F12)
- [ ] Network tab open
- [ ] Tried with NEW email (not used before)
- [ ] Password is 8+ characters
- [ ] Passwords match

---

**Do the tests above and send me the console output!** 🔍

The console logs will tell us EXACTLY what's wrong.

