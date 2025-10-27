# 🔧 Detailed Setup Guide

## Step-by-Step Installation

### Part 1: Install Python (Skip if already installed)

1. **Check if Python is installed:**
   ```bash
   python --version
   ```
   You need Python 3.11 or higher.

2. **If not installed:**
   - Windows: Download from [python.org](https://www.python.org/downloads/)
   - Mac: `brew install python3.11`
   - Linux: `sudo apt install python3.11`

---

### Part 2: Install PostgreSQL

1. **Download PostgreSQL:**
   - Visit [postgresql.org](https://www.postgresql.org/download/)
   - Download the installer for your OS
   - During installation, remember your password!

2. **Verify Installation:**
   ```bash
   psql --version
   ```

3. **Create Your Database:**
   ```bash
   # Open PostgreSQL command line
   # Windows: Use "SQL Shell (psql)" from Start menu
   # Mac/Linux: Run 'psql postgres' in terminal
   
   CREATE DATABASE clinic_saas;
   ```

   **Hint**: If you get "command not found", add PostgreSQL to your PATH:
   - Windows: `C:\Program Files\PostgreSQL\15\bin`
   - Mac: Usually automatic with Homebrew
   - Linux: Usually automatic with apt

---

### Part 3: Set Up Your Project

1. **Navigate to Your Project:**
   ```bash
   cd "d:\clinic multi tennant SaaS"
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```
   
   **What is this?** A virtual environment keeps your project's dependencies separate from other Python projects. Think of it as a sandbox!

3. **Activate Virtual Environment:**
   ```bash
   # Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   
   # Windows (Command Prompt):
   venv\Scripts\activate.bat
   
   # Mac/Linux:
   source venv/bin/activate
   ```
   
   **You'll know it worked** when you see `(venv)` at the start of your command line!

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will take a few minutes. It's installing FastAPI, SQLAlchemy, and other tools.

---

### Part 4: Configure Environment Variables

1. **Copy the example file:**
   ```bash
   # Windows:
   copy .env.example .env
   
   # Mac/Linux:
   cp .env.example .env
   ```

2. **Edit `.env` file** with your favorite text editor:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/clinic_saas
   SECRET_KEY=your-super-secret-key-change-this
   ```

   **Replace:**
   - `username`: Your PostgreSQL username (default: `postgres`)
   - `password`: Your PostgreSQL password
   - `clinic_saas`: Your database name
   - `your-super-secret-key-change-this`: Generate a random string (at least 32 characters)

   **Tip**: To generate a secret key, run:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

---

### Part 5: Run Your First Server

1. **Start the development server:**
   ```bash
   uvicorn app.main:app --reload
   ```

   **What does this mean?**
   - `app.main` → Look in the `app` folder for `main.py`
   - `app` → The FastAPI application object
   - `--reload` → Automatically restart when you change code

2. **Visit these URLs:**
   - http://localhost:8000 → Your API
   - http://localhost:8000/docs → **Interactive API documentation** (Swagger UI)
   - http://localhost:8000/redoc → Alternative documentation

---

## 🎓 Understanding the Workflow

### The Development Loop

```
1. Write code in your editor
2. Server auto-reloads (thanks to --reload)
3. Test in browser at /docs
4. Check terminal for errors
5. Fix and repeat!
```

### How to Test Your API

1. **Option 1: Swagger UI** (Easiest!)
   - Go to http://localhost:8000/docs
   - Click on an endpoint
   - Click "Try it out"
   - Fill in parameters
   - Click "Execute"

2. **Option 2: Postman**
   - Download [Postman](https://www.postman.com/downloads/)
   - Create a new request
   - Enter URL: http://localhost:8000/your-endpoint
   - Select HTTP method (GET, POST, etc.)
   - Add body/headers as needed
   - Send!

3. **Option 3: Python Requests**
   ```python
   import requests
   
   response = requests.get("http://localhost:8000/health")
   print(response.json())
   ```

---

## 🐛 Troubleshooting

### Problem: "python: command not found"
**Solution**: Python isn't in your PATH. Try `python3` instead of `python`.

### Problem: "psql: command not found"
**Solution**: PostgreSQL isn't in your PATH. Add it:
- Windows: Add `C:\Program Files\PostgreSQL\15\bin` to PATH
- Mac: Reinstall with Homebrew
- Linux: `sudo apt install postgresql-client`

### Problem: "connection refused" when connecting to database
**Solution**: PostgreSQL isn't running.
- Windows: Open Services, start PostgreSQL service
- Mac: `brew services start postgresql`
- Linux: `sudo systemctl start postgresql`

### Problem: "Permission denied" when activating venv
**Solution** (Windows PowerShell):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: Port 8000 already in use
**Solution**: Use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Problem: "No module named 'app'"
**Solution**: Make sure you're in the project root directory and `app/__init__.py` exists.

---

## 🎯 Your First Tasks

Once setup is complete:

1. **Task 1**: Make sure the server runs without errors
2. **Task 2**: Visit http://localhost:8000/docs and see the auto-generated documentation
3. **Task 3**: Open `app/main.py` and read the TODO comments
4. **Task 4**: Try to add a simple "Hello World" endpoint on your own!

**Hint for Task 4:**
```python
@app.get("/hello")
async def hello():
    return {"message": "Hello World!"}
```

Try to figure out where this goes in `main.py` by looking at the structure!

---

## 📚 Useful Commands Reference

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

# Install packages
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Run server
uvicorn app.main:app --reload

# Run tests (later)
pytest

# Database migrations (later)
alembic upgrade head
```

---

## 🎉 You're Ready!

If you can:
- ✅ Activate your virtual environment
- ✅ Run the server without errors
- ✅ See the docs at /docs

**Then you're ready to start coding!** 

Open `app/main.py` and start with the TODOs there. Take it step by step, and don't hesitate to Google things. Learning to search for solutions is a crucial developer skill!

Good luck! 🚀

