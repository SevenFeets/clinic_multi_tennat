"""
Create endpoints for user registration and login
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user
from app.models.tenant import Tenant
from app.schemas import user as user_schema
from app.utils.security import hash_password, verify_password, create_access_token
from app.auth.dependencies import get_current_active_user, require_tenant

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
async def register(user_data: user_schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(user.User).filter(user.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
            )
    
    tenant = db.query(Tenant).filter(Tenant.id == user_data.tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with ID {user_data.tenant_id} not found"
        )
    
    if not tenant.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tenant '{tenant.name}' is not active. Registration is disabled."
        )

    hashed_password = hash_password(user_data.password)
    new_user = user.User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        # TODO: Implement proper email verification flow:
        #   1. Generate verification token after registration
        #   2. Send verification email with token link
        #   3. Create /verify-email endpoint that sets is_active=True
        #   4. Remove is_active=True from here
        is_active=True,
        tenant_id=user_data.tenant_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=user_schema.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_existing_user = db.query(user.User).filter(user.User.email == form_data.username).first()
    if not db_existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(form_data.password, db_existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not db_existing_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(data={"sub": db_existing_user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": db_existing_user}


@router.get("/me", response_model=user_schema.User)
async def get_me(current_user: user.User = Depends(require_tenant)) -> user.User:
    """Get current user information."""
    return current_user


@router.patch("/me", response_model=user_schema.User)
async def update_profile(
    user_update: user_schema.UserUpdate,
    current_user: user.User = Depends(require_tenant),
    db: Session = Depends(get_db)
):
    """Update current user's profile."""
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(user.User).filter(
            user.User.email == user_update.email,
            user.User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.patch("/me/password", response_model=user_schema.User)
async def change_password(
    password_data: user_schema.PasswordChange,
    current_user: user.User = Depends(require_tenant),
    db: Session = Depends(get_db)
):
    """Change current user's password."""
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect current password"
        )
    
    current_user.hashed_password = hash_password(password_data.new_password)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user
