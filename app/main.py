from fastapi import FastAPI
from datetime import datetime

from fastapi.middleware.cors import CORSMiddleware

from app.middleware.tenant import TenantMiddleware

from app.api import auth, patients, appointments, stats, waitlist, recurring_appointments, calendar

from app.services.scheduler_service import start_scheduler, stop_scheduler

try:
    from prometheus_fastapi_instrumentator import Instrumentator  # pyright: ignore[reportMissingImports]
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

app = FastAPI(title="Clinic Management API", version="1.0.0")

if PROMETHEUS_AVAILABLE:
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)

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
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)


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


@app.on_event("startup")
async def startup_event():
    """Start background services when app starts"""
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
