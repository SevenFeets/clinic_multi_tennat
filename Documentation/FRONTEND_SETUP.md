# 🎨 Frontend Setup Guide

## ⚠️ Prerequisites: Install Node.js

Before we can create the React frontend, you need Node.js installed.

---

## 📥 **Step 1: Download Node.js**

### **Option A: Official Installer (Recommended)**

1. Visit: https://nodejs.org/
2. Download: **LTS version** (Long Term Support) - Currently v20.x
3. Run the installer
4. Accept all defaults
5. **Restart your terminal/PowerShell after installation**

### **Option B: Using Winget (Windows Package Manager)**

```powershell
# If you have winget installed
winget install OpenJS.NodeJS.LTS
```

### **Option C: Using Chocolatey**

```powershell
# If you have chocolatey installed
choco install nodejs-lts
```

---

## ✅ **Step 2: Verify Installation**

After installing, **close and reopen your terminal**, then run:

```powershell
node --version
# Should show: v20.x.x or v18.x.x

npm --version
# Should show: 10.x.x or 9.x.x
```

---

## 🚀 **Step 3: Create React Frontend**

Once Node.js is installed, run these commands:

```powershell
# Navigate to project root
cd "D:\clinic multi tennant SaaS"

# Make sure you're on frontend branch
git checkout frontend

# Create React app (choose ONE method)
```

### **Method 1: Create React App** (Easiest for beginners)
```powershell
npx create-react-app frontend
```
- ✅ Well documented
- ✅ Battle-tested
- ✅ Beginner-friendly
- ❌ Slower than Vite

### **Method 2: Vite** (Modern, faster)
```powershell
npm create vite@latest frontend -- --template react
```
- ✅ Very fast
- ✅ Modern tooling
- ✅ Smaller bundle size
- ❌ Less beginner resources

### **Method 3: Next.js** (If you want server-side rendering)
```powershell
npx create-next-app@latest frontend
```
- ✅ Great for SEO
- ✅ Server-side rendering
- ✅ Professional choice
- ❌ More complex

**Recommendation for learning: Use Create React App (Method 1)**

---

## 📁 **Step 4: Project Structure After Setup**

After creating the frontend, your structure will be:

```
D:\clinic multi tennant SaaS\
│
├── app/                  # Backend (FastAPI)
├── alembic/              # Database migrations
├── scripts/              # Helper scripts
├── Documentation/        # Project docs
├── myvenv/              # Python virtual environment
├── requirements.txt     # Python dependencies
│
└── frontend/            # ← NEW! React app
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── App.js
    │   └── index.js
    ├── package.json
    └── README.md
```

---

## 🔧 **Step 5: Configure API Connection**

Create `.env` file in `frontend/` folder:

```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TENANT_ID=cityclinic
```

---

## 🎯 **Step 6: Start Development Servers**

### **Terminal 1: Backend**
```powershell
cd "D:\clinic multi tennant SaaS"
myvenv\Scripts\activate
uvicorn app.main:app --reload
```
Backend runs at: http://localhost:8000

### **Terminal 2: Frontend**
```powershell
cd "D:\clinic multi tennant SaaS\frontend"
npm start
```
Frontend runs at: http://localhost:3000

---

## 📝 **Step 7: Update .gitignore**

Add to root `.gitignore`:

```
# Frontend
frontend/node_modules/
frontend/build/
frontend/dist/
frontend/.env.local
frontend/.env.development.local
frontend/.env.test.local
frontend/.env.production.local
```

---

## ✅ **Step 8: First Commit**

```powershell
git add frontend/
git add .gitignore
git commit -m "feat: Initialize React frontend application"
git push origin frontend
```

---

## 🔗 **Step 9: Connect to Backend API**

Create API service file:

```javascript
// frontend/src/services/api.js
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const login = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);
  
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  });
  
  return response.json();
};

export const getPatients = async (token, tenantId) => {
  const response = await fetch(`${API_URL}/patients`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'X-Tenant-ID': tenantId,
    },
  });
  
  return response.json();
};
```

---

## 🎨 **Recommended UI Libraries**

After basic setup, consider adding:

### **For Styling:**
- **Tailwind CSS** (utility-first) - Recommended!
- **Material-UI** (component library)
- **Chakra UI** (accessible components)

### **For State Management:**
- **React Context** (built-in, simple)
- **Zustand** (modern, simple)
- **Redux Toolkit** (complex apps)

### **For Forms:**
- **React Hook Form** (performant)
- **Formik** (popular)

### **For Data Fetching:**
- **TanStack Query (React Query)** - Highly recommended!
- **SWR** (by Vercel)
- **Axios** (simple)

---

## 📚 **Learning Resources**

### **React Basics:**
- Official Tutorial: https://react.dev/learn
- FreeCodeCamp: https://www.freecodecamp.org/news/react-tutorial/

### **Connecting to APIs:**
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- React Query: https://tanstack.com/query/latest

### **Styling:**
- Tailwind CSS: https://tailwindcss.com/docs
- CSS-Tricks: https://css-tricks.com/

---

## 🐛 **Troubleshooting**

### **Issue: "npm not recognized"**
- **Solution**: Restart terminal after installing Node.js

### **Issue: Port 3000 already in use**
```powershell
# Use different port
PORT=3001 npm start
```

### **Issue: CORS errors in browser**
- **Solution**: Your FastAPI CORS is already configured for localhost:3000

### **Issue: API connection fails**
- Check backend is running: http://localhost:8000/docs
- Check frontend .env file has correct API_URL
- Check browser console for errors

---

## ✅ **Checklist**

Before starting frontend development:

- [ ] Node.js installed (v18+ or v20+)
- [ ] npm installed (comes with Node.js)
- [ ] `frontend` git branch created
- [ ] React app created in `frontend/` folder
- [ ] .gitignore updated
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can see React welcome page in browser

---

## 🎯 **Next Steps After Setup**

1. **Week 5**: Build login page
2. **Week 5**: Create dashboard layout
3. **Week 6**: Build patient list page
4. **Week 6**: Build appointment calendar
5. **Week 7**: Add forms and validation
6. **Week 8**: Polish UI/UX

---

## 💡 **Pro Tips**

1. **Use VS Code Extensions:**
   - ES7+ React/Redux/React-Native snippets
   - Tailwind CSS IntelliSense
   - Prettier

2. **Install React DevTools:**
   - Chrome extension for debugging React

3. **Learn React Hooks:**
   - useState, useEffect are essential
   - Custom hooks for reusable logic

4. **Component Organization:**
   ```
   src/
   ├── components/     # Reusable UI components
   ├── pages/          # Page components
   ├── services/       # API calls
   ├── hooks/          # Custom React hooks
   ├── utils/          # Helper functions
   └── context/        # Global state
   ```

---

**Once Node.js is installed, come back and I'll help you create the React app!** 🚀

