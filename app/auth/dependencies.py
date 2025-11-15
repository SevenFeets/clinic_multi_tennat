"""
Authentication Dependencies - Protect routes and get current user
- Dependencies = Functions that run before your endpoint
- Use them to verify authentication
- FastAPI passes the result to your endpoint
- Reusable across all protected routes
"""

# Import necessary modules

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Session
from app.database import get_db
from app.utils.security import verify_token
from app.models.user import User 


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

    #verify token
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    # get email from token
    email: str = payload.email
    if email is None:
        raise credentials_exception

    # get user from database
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
            header={"WWW-Authenticate": "Bearer"}
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
            header={"WWW-Authenticate": "Bearer"}
        )

    return current_user

#  require_tenant (ensure user belongs to tenant)

# TODO

#  rate_limiting (prevent abuse)

# TODO



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

