"""
Tenant Middleware - Automatically identify and set tenant context

Middleware that runs before every request to identify which tenant (clinic)
is making the request and store that context for the endpoint to use.
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.database import SessionLocal
from app.models.tenant import Tenant
from app.models.user import User


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware to identify tenant from request and store in request.state.
    
    For development, we use a custom header: X-Tenant-ID
    In production, you might use subdomain instead.
    """
    
    EXCLUDED_PATHS = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/health",
        "/",
        "/favicon.ico"
    ]
    
    async def dispatch(self, request: Request, call_next):
        """Process each request to extract and validate tenant."""
        
        if request.method == "OPTIONS":
            return await call_next(request)
        
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        if request.url.path.startswith(("/static", "/api/openapi")):
            return await call_next(request)
        
        tenant_subdomain = request.headers.get("X-Tenant-ID")
        
        if not tenant_subdomain:
            if request.url.path.startswith("/auth/register") or request.url.path.startswith("/auth/login"):
                return await call_next(request)
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant identifier missing. Please provide X-Tenant-ID header."
            )
        
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
            
            request.state.tenant = tenant
            request.state.tenant_id = tenant.id
            
            response = await call_next(request)
            
            response.headers["X-Tenant-ID"] = tenant.subdomain
            response.headers["X-Tenant-Name"] = tenant.name
            
            return response
            
        finally:
            db.close()

#  UNDERSTANDING MIDDLEWARE:
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




