# 🚀 Quick Start Guide

## Your First 30 Minutes

Follow these steps to get your project running RIGHT NOW:

### Step 1: Open Terminal (5 minutes)

1. Open PowerShell or Command Prompt
2. Navigate to your project:
   ```bash
   cd "d:\clinic multi tennant SaaS"
   ```

### Step 2: Create Virtual Environment (5 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it (PowerShell)
.\venv\Scripts\Activate.ps1

# You should see (venv) at start of your prompt
```

**Stuck?** If you get "execution policy" error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies (10 minutes)

```bash
# This will take a few minutes
pip install -r requirements.txt

# Wait for all packages to install...
```

**Stuck?** If pip fails:
- Make sure you're in the virtual environment (see `(venv)`)
- Try: `python -m pip install --upgrade pip`
- Then retry: `pip install -r requirements.txt`

### Step 4: Set Up PostgreSQL (Optional for now)

**Don't have PostgreSQL yet?** Skip this for now! You can install it later and start with the code first.

If you have PostgreSQL:
```bash
# Copy the environment file
copy env.example .env

# Edit .env with your database credentials
# Use Notepad or VS Code to edit .env
```

### Step 5: Your First Code! (10 minutes)

Open `app/main.py` in your favorite editor and follow the TODOs!

Here's what you need to do:
1. Import FastAPI
2. Create app instance
3. Create a health check endpoint

**Hint**: Look at the comments in the file - they guide you step by step!

### Step 6: Run the Server

```bash
uvicorn app.main:app --reload
```

**Success looks like:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 7: See Your API in Action!

Open your browser and go to:
- http://localhost:8000/docs

You'll see **automatic API documentation**! This is one of FastAPI's superpowers! 🎉

---

## What You Just Did

✅ Created an isolated Python environment  
✅ Installed FastAPI and dependencies  
✅ Set up your project structure  
✅ Got automatic API documentation  

---

## Next Steps

### Today:
1. Complete the TODOs in `app/main.py`
2. Add a few simple endpoints
3. Test them in the `/docs` interface

### This Week:
1. Read through all the template files
2. Set up PostgreSQL
3. Complete `app/database.py`
4. Create your first database table

### This Month:
Follow the week-by-week guide in `README.md`!

---

## Common First-Day Issues

### "Command not found: python"
Try `python3` instead of `python`

### "Cannot activate venv"
Make sure you're in the project directory first

### "Import errors when running"
Make sure virtual environment is activated (you should see `(venv)`)

### "I don't understand the TODOs"
That's normal! Start with:
1. Read the FastAPI tutorial link in the TODO
2. Look at the HINT comments
3. Google "FastAPI [what you're trying to do]"
4. Try something - it's okay to make mistakes!

---

## Pro Tips 💡

1. **Keep the server running**: The `--reload` flag means it restarts automatically when you save files
2. **Use /docs liberally**: Test every change immediately in the browser
3. **Read error messages**: Python errors tell you exactly what's wrong
4. **Commit often**: Once something works, commit it to Git!
5. **One TODO at a time**: Don't try to do everything at once

---

## Your First Achievement 🏆

Once you have a working endpoint at http://localhost:8000/docs - **CONGRATULATIONS!** 

You just:
- Set up a professional Python environment
- Installed a modern web framework
- Created a web API
- Got automatic API documentation

That's legitimately impressive for someone who just learned Python basics!

---

## Need Help?

**Stuck on something?**
1. Read the error message carefully
2. Check the HINTS in the TODO comments
3. Google: "FastAPI [your problem]"
4. Check the learning resources in README.md

**Remember**: Every developer Googles things constantly. It's not cheating - it's how development works!

---

## Ready to Code?

Open `app/main.py` and let's build something awesome! 🚀

**Start with the first TODO and work your way down. You've got this!** 💪

