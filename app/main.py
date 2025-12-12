
# Import FastAPI
from fastapi import FastAPI
from datetime import datetime

# Import CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# Import tenant middleware
from app.middleware.tenant import TenantMiddleware

# Import routers
from app.api import auth, patients, appointments

# Create FastAPI app instance
app = FastAPI(title="Clinic Management API", version="1.0.0")

# Include routers
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(appointments.router)

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
        "http://localhost:3000",  # React default port
        "http://localhost:3001",  # Alternative frontend port
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

# 🧪 TESTING YOUR WORK:
# 1. Run: uvicorn app.main:app --reload
# 2. Visit: http://localhost:8000/docs
# 3. Try out your endpoints in the interactive documentation!
# 4. You should see your endpoints listed and be able to test them

