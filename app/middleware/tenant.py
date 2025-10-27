"""
Tenant Middleware - Automatically identify and set tenant context

🎯 YOUR MISSION (Week 3):
Create middleware to handle multi-tenant routing

📚 LEARNING RESOURCES:
- FastAPI Middleware: https://fastapi.tiangolo.com/tutorial/middleware/
- Middleware Basics: https://www.youtube.com/watch?v=3vfum74ggHE

💡 KEY CONCEPTS:
- Middleware = Code that runs for every request
- Extract tenant from subdomain or header
- Make tenant available to all endpoints
- Reject requests with invalid tenant
"""

# TODO: Import necessary modules
# HINT: from fastapi import Request, HTTPException
# HINT: from starlette.middleware.base import BaseHTTPMiddleware
# HINT: from app.database import SessionLocal
# HINT: from app.models.tenant import Tenant


# TODO: Create TenantMiddleware class
# HINT: class TenantMiddleware(BaseHTTPMiddleware):
# HINT:     async def dispatch(self, request: Request, call_next):
# HINT:         
# HINT:         # Extract tenant identifier (subdomain or header)
# HINT:         # Option 1: From subdomain
# HINT:         # host = request.headers.get("host", "")
# HINT:         # subdomain = host.split(".")[0]
# HINT:         
# HINT:         # Option 2: From custom header (easier for development)
# HINT:         tenant_subdomain = request.headers.get("X-Tenant-ID", "default")
# HINT:         
# HINT:         # Verify tenant exists
# HINT:         db = SessionLocal()
# HINT:         try:
# HINT:             tenant = db.query(Tenant).filter(
# HINT:                 Tenant.subdomain == tenant_subdomain,
# HINT:                 Tenant.is_active == True
# HINT:             ).first()
# HINT:             
# HINT:             if not tenant:
# HINT:                 raise HTTPException(status_code=404, detail="Tenant not found")
# HINT:             
# HINT:             # Store tenant in request state
# HINT:             request.state.tenant = tenant
# HINT:             
# HINT:             # Continue to endpoint
# HINT:             response = await call_next(request)
# HINT:             return response
# HINT:         finally:
# HINT:             db.close()


# 📖 UNDERSTANDING MIDDLEWARE:
# 
# Request Flow with Middleware:
# 1. Request comes in
# 2. Middleware extracts tenant
# 3. Middleware verifies tenant exists
# 4. Middleware stores tenant in request.state
# 5. Endpoint runs with tenant context
# 6. Response goes back
#
# Subdomain Routing:
# - clinic1.yourapp.com → tenant_id = 1
# - clinic2.yourapp.com → tenant_id = 2
# - admin.yourapp.com → special handling
#
# Header-Based (easier for development):
# - Send "X-Tenant-ID: clinic1" header
# - Good for testing and mobile apps
# - Can switch tenants easily

# 🎯 CHALLENGE:
# Add features:
# - Tenant usage tracking (request count)
# - Rate limiting per tenant
# - Tenant-specific configuration
# - Subdomain validation

# ⚠️ IMPORTANT:
# - Always verify tenant is active
# - Handle missing tenant gracefully
# - Log tenant access for security
# - Cache tenant lookups for performance

# 💡 USAGE IN ENDPOINTS:
# def some_endpoint(request: Request):
#     tenant = request.state.tenant
#     # Now you have tenant info!

# 🧪 TESTING:
# Use Postman or curl:
# curl -H "X-Tenant-ID: clinic1" http://localhost:8000/patients
#
# In Swagger UI, you'll need to add custom headers
# or disable this middleware for development

