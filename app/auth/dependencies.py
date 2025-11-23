"""
Authentication Dependencies - Protect routes and get current user
- Dependencies = Functions that run before your endpoint
- Use them to verify authentication
- FastAPI passes the result to your endpoint
- Reusable across all protected routes
"""

# Import necessary modules
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import verify_token
from app.models.user import User
from app.models.tenant import Tenant 


# Create OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") # login endpoint

# Dependency to get current user from token
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    # Create exception for authentication failures 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Verify token and extract user data
    # verify_token() returns TokenData with email, or None if invalid
    # If None is returned, the token is invalid (expired, bad signature, or missing email)
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    # At this point, payload.email is guaranteed to be not None
    # (verify_token already checks this internally)
    email: str = payload.email  # Type is str, not Optional[str]

    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user

# Dependency to get active user only
async def get_current_active_user(
    current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return current_user

#  get_current_superuser (only admins)
async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return current_user

# Dependency to get tenant from request (set by middleware)
async def get_tenant(request: Request) -> Tenant:
    """
    Get the current tenant from request.state.
    The tenant is set by TenantMiddleware.
    
    Usage:
        @app.get("/endpoint")
        async def my_endpoint(tenant: Tenant = Depends(get_tenant)):
            return {"tenant": tenant.name}
    """
    if not hasattr(request.state, "tenant"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context not found. Please provide X-Tenant-ID header."
        )
    
    return request.state.tenant


# Dependency to verify user belongs to current tenant
async def require_tenant(
    request: Request,
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Verify that the current user belongs to the tenant in the request context.
    Returns the user if they belong to the tenant, raises exception otherwise.
    
    Usage:
        @app.get("/protected-endpoint")
        async def my_endpoint(user: User = Depends(require_tenant)):
            # user is guaranteed to belong to the tenant in the request
            return {"message": f"Hello {user.full_name}"}
    
    Security:
        - Prevents users from accessing other tenants' data
        - Critical for multi-tenant data isolation
    """
    if not hasattr(request.state, "tenant"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant context not found"
        )
    
    tenant: Tenant = request.state.tenant
    
    # Check if user belongs to this tenant
    if current_user.tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not assigned to any tenant. Please contact support."
        )
    
    if current_user.tenant_id != tenant.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. User does not belong to tenant '{tenant.name}'"
        )
    
    return current_user


#  rate_limiting (prevent abuse)
# TODO: Implement rate limiting in Month 4 (Production Hardening)



# 📖 UNDERSTANDING DEPENDENCIES:
# 
# How to use these in endpoints:
# 
# @app.get("/protected")
# async def protected_route(current_user: User = Depends(get_current_active_user)):
#     return {"message": f"Hello {current_user.email}"}
# 
# What happens:
# 1. Client sends request with Authorization header
# 2. oauth2_scheme extracts the token
# 3. get_current_user verifies token and fetches user
# 4. get_current_active_user checks if user is active
# 5. Your endpoint receives the user object
# 
# If any step fails → 401 Unauthorized error

# 🎯 CHALLENGE:
# Add dependencies for:
# - get_current_superuser (only admins)
# - require_tenant (ensure user belongs to tenant)
# - rate_limiting (prevent abuse)

# 🧪 TESTING:
# 1. Login to get a token
# 2. Use token in Authorization header: "Bearer <token>"
# 3. Call protected endpoint
# 4. Try with invalid token → should get 401 error

# 💡 TIP:
# In Swagger UI (/docs):
# - Click the "Authorize" button
# - Enter your token
# - Now you can test protected endpoints!

