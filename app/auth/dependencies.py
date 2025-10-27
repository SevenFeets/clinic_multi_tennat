"""
Authentication Dependencies - Protect routes and get current user

🎯 YOUR MISSION (Week 2):
Create dependencies to protect API endpoints

📚 LEARNING RESOURCES:
- FastAPI Dependencies: https://fastapi.tiangolo.com/tutorial/dependencies/
- OAuth2 Password Bearer: https://fastapi.tiangolo.com/tutorial/security/first-steps/

💡 KEY CONCEPTS:
- Dependencies = Functions that run before your endpoint
- Use them to verify authentication
- FastAPI passes the result to your endpoint
- Reusable across all protected routes
"""

# TODO: Import necessary modules
# HINT: from fastapi import Depends, HTTPException, status
# HINT: from fastapi.security import OAuth2PasswordBearer
# HINT: from sqlalchemy.orm import Session
# HINT: from app.database import get_db
# HINT: from app.auth.auth import verify_token
# HINT: from app.models.user import User
# HINT: from app.schemas.user import TokenData


# TODO: Create OAuth2 scheme
# HINT: oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
# NOTE: This tells FastAPI where the login endpoint is


# TODO: Dependency to get current user from token
# HINT: async def get_current_user(
# HINT:     token: str = Depends(oauth2_scheme),
# HINT:     db: Session = Depends(get_db)
# HINT: ) -> User:
# HINT:     
# HINT:     # Create exception for authentication failures
# HINT:     credentials_exception = HTTPException(
# HINT:         status_code=status.HTTP_401_UNAUTHORIZED,
# HINT:         detail="Could not validate credentials",
# HINT:         headers={"WWW-Authenticate": "Bearer"},
# HINT:     )
# HINT:     
# HINT:     # Verify token
# HINT:     payload = verify_token(token)
# HINT:     if payload is None:
# HINT:         raise credentials_exception
# HINT:     
# HINT:     # Get email from token
# HINT:     email: str = payload.get("sub")
# HINT:     if email is None:
# HINT:         raise credentials_exception
# HINT:     
# HINT:     # Get user from database
# HINT:     user = db.query(User).filter(User.email == email).first()
# HINT:     if user is None:
# HINT:         raise credentials_exception
# HINT:     
# HINT:     return user


# TODO: Dependency to get active user only
# HINT: async def get_current_active_user(
# HINT:     current_user: User = Depends(get_current_user)
# HINT: ) -> User:
# HINT:     if not current_user.is_active:
# HINT:         raise HTTPException(status_code=400, detail="Inactive user")
# HINT:     return current_user


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

