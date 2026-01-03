
# Import FastAPI
from fastapi import FastAPI
from datetime import datetime

# Import CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# Import tenant middleware
from app.middleware.tenant import TenantMiddleware

# Import routers
from app.api import auth, patients, appointments, stats, waitlist, recurring_appointments, calendar

# Import scheduler
from app.services.scheduler_service import start_scheduler, stop_scheduler

# Create FastAPI app instance
app = FastAPI(title="Clinic Management API", version="1.0.0")

# Include routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(stats.router)
app.include_router(waitlist.router)
app.include_router(recurring_appointments.router)
app.include_router(calendar.router)

# Add middlewares (ORDER MATTERS!)
# ⚠️ CRITICAL: Middleware executes in REVERSE order (last added = first executed)
# We want: Request → CORS → Tenant → Endpoint
# So we add: Tenant first, CORS second

# 1. Add TenantMiddleware FIRST (so it executes LAST, after CORS)
app.add_middleware(TenantMiddleware)

# 2. Add CORSMiddleware SECOND (so it executes FIRST, handles preflight)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:5174",  # Vite alternative port
        "http://localhost:3000",  # React (Create React App) default port
        "http://localhost:3001",  # Alternative frontend port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)


# Public endpoints (no tenant required)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}


@app.get("/")
async def main():
    return {"message": "Welcome to the Clinic Management API"}
@app.get("/datetime")
async def get_datetime():
    return {"datetime": str(datetime.now())}


@app.get("/about")
async def about():
    return {"message": "This is the about page"}

@app.get("/contact")
async def contact():
    return {"message": "This is the contact page"}

@app.get("/services")
async def services():
    return {"message": "This is the services page"}

@app.get("/products")
async def products():
    return {"message": "This is the products page"}


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Start background services when app starts"""
    # Start scheduler for automated reminders
    try:
        start_scheduler()
    except Exception as e:
        print(f"Warning: Could not start scheduler: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop background services when app shuts down"""
    try:
        stop_scheduler()
    except Exception as e:
        print(f"Warning: Error stopping scheduler: {e}")

# 🧪 TESTING YOUR WORK:
# 1. Run: uvicorn app.main:app --reload
# 2. Visit: http://localhost:8000/docs
# 3. Try out your endpoints in the interactive documentation!
# 4. You should see your endpoints listed and be able to test them

