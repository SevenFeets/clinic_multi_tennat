"""
Tenant Middleware - Automatically identify and set tenant context

Middleware that runs before every request to identify which tenant (clinic)
is making the request and store that context for the endpoint to use.
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import SessionLocal
from app.models.tenant import Tenant
from app.models.user import User  # Import to resolve relationships


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware to identify tenant from request and store in request.state.
    
    For development, we use a custom header: X-Tenant-ID
    In production, you might use subdomain instead.
    """
    
    # Paths that don't require tenant context
    EXCLUDED_PATHS = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/health",
        "/",
        "/favicon.ico"
    ]
    
    async def dispatch(self, request: Request, call_next):
        """
        Process each request to extract and validate tenant.
        
        Flow:
        1. Check if path requires tenant
        2. Extract tenant identifier from header
        3. Query database for tenant
        4. Verify tenant is active
        5. Store tenant in request.state
        6. Continue to endpoint
        """
        
        # Skip tenant checking for CORS preflight requests (OPTIONS method)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Skip tenant checking for public paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        # Also skip for static files and OpenAPI schema
        if request.url.path.startswith(("/static", "/api/openapi")):
            return await call_next(request)
        
        # Extract tenant identifier from custom header (easier for development)
        # In production, you might use: subdomain = request.url.hostname.split(".")[0]
        tenant_subdomain = request.headers.get("X-Tenant-ID")
        
        if not tenant_subdomain:
            # For auth endpoints, we might not need tenant yet (during registration)
            # Allow auth endpoints without tenant
            if request.url.path.startswith("/auth/register") or request.url.path.startswith("/auth/login"):
                return await call_next(request)
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant identifier missing. Please provide X-Tenant-ID header."
            )
        
        # Query database for tenant
        db = SessionLocal()
        try:
            tenant = db.query(Tenant).filter(
                Tenant.subdomain == tenant_subdomain,
                Tenant.is_active == True
            ).first()
            
            if not tenant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tenant '{tenant_subdomain}' not found or inactive"
                )
            
            # Store tenant in request state (available to all endpoints)
            request.state.tenant = tenant
            request.state.tenant_id = tenant.id
            
            # Continue to the endpoint
            response = await call_next(request)
            
            # Optional: Add tenant info to response headers for debugging
            response.headers["X-Tenant-ID"] = tenant.subdomain
            response.headers["X-Tenant-Name"] = tenant.name
            
            return response
            
        finally:
            db.close()


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

