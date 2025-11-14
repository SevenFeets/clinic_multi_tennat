"""
Create endpoints for user registration and login
"""

# Import FastAPI components
import http
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Import your modules
from app.database import get_db
from app.models import user
from app.schemas import user as user_schema
from app.utils.security import hash_password, verify_password, create_access_token
from app.auth.dependencies import get_current_active_user

#Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Registration endpoint
@router.post("/register", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
async def register(user_data: user_schema.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(user.User).filter(user.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
            )

    #create new user
    hashed_password = hash_password(user_data.password)
    new_user = user.User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login endpoint
@router.post("/login", response_model=user_schema.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #find user by email
    db_existing_user = db.query(user.User).filter(user.User.email == form_data.username).first()
    if not db_existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            header={"WWW-Authenticate": "Bearer"}
        )

    #verify password
    if not verify_password(form_data.password, db_existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            header={"WWW-Authenticate": "Bearer"}
        )

    # check if user is active
    if not db_existing_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            header={"WWW-Authenticate": "Bearer"}
        )

    # create access token
    access_token = create_access_token(data={"sub": db_existing_user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": db_existing_user}


#  Get current user endpoint (test authentication)
# @router.get("/me", response_model=user_schema.User)
# async def get_me(current_user: user.User = Depends(get_current_active_user)):
# return current_user

# HINT: @router.get("/me", response_model=UserSchema)
# HINT: async def get_me(current_user: User = Depends(get_current_active_user)):
# HINT:     return current_user
# NOTE: Don't forget to import get_current_active_user from dependencies!


# 📖 UNDERSTANDING THE FLOW:
# 
# Registration:
# 1. Client sends email + password
# 2. Server checks if email exists
# 3. Server hashes password
# 4. Server creates user in database
# 5. Server returns user info (no password!)
#
# Login:
# 1. Client sends email + password
# 2. Server finds user by email
# 3. Server verifies password hash
# 4. Server creates JWT token
# 5. Client stores token
#
# Using Protected Routes:
# 1. Client sends token in Authorization header
# 2. Server verifies token
# 3. Server executes endpoint with user info

# 🎯 CHALLENGE:
# Add endpoints for:
# - Password reset request
# - Password reset confirm
# - Email verification
# - Logout (token blacklist)

# ⚠️ SECURITY TIPS:
# - Always hash passwords before storing
# - Use generic error messages ("Incorrect email or password")
#   Don't say "Email not found" (security through obscurity)
# - Add rate limiting to prevent brute force
# - Log failed login attempts

# 🧪 TESTING IN SWAGGER UI:
# 1. Go to /docs
# 2. Try POST /auth/register with email and password
# 3. Try POST /auth/login with same credentials
# 4. Copy the access_token from response
# 5. Click "Authorize" button, paste token
# 6. Try GET /auth/me to see your user info

# 💡 COMMON ISSUES:
# - "422 Unprocessable Entity": Check your request body format
# - "401 Unauthorized": Token is invalid or expired
# - "400 Bad Request": Email already exists or user inactive

