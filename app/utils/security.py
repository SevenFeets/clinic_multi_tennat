"""
Security Utilities - Password Hashing and JWT Tokens

Create security functions for authentication

📚 KEY CONCEPTS:
- Password Hashing: One-way encryption (can't be reversed!)
- JWT Tokens: Secure way to keep users logged in
- Bcrypt: Industry standard for password hashing

🔒 SECURITY PRINCIPLES:
1. NEVER store plain passwords
2. NEVER log passwords (even hashed ones)
3. Use strong encryption algorithms
4. Set token expiration times
"""

# ============================================================================
# IMPORTS - The Tools We Need
# ============================================================================

# Password hashing with bcrypt (industry standard)
from passlib.context import CryptContext

# JWT token creation and verification
from jose import JWTError, jwt

# Date/time handling for token expiration
from datetime import datetime, timedelta, timezone

# Type hints for better code quality
from typing import Optional

# Our app configuration (SECRET_KEY, etc.)
from app.config import settings

# Our schemas for type checking
from app.schemas.user import TokenData


# ============================================================================
# CONFIGURATION - How We Hash Passwords
# ============================================================================

# Create a password context using bcrypt
# - bcrypt is slow on purpose (makes brute-force attacks harder)
# - deprecated="auto" means it will auto-upgrade to newer bcrypt versions
pwd_context = CryptContext(
    schemes=["bcrypt", "argon2"],
    default="bcrypt",
    deprecated="auto"
)


# ============================================================================
# PART 1: PASSWORD HASHING
# ============================================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain password matches its hash.
    
    🔍 HOW IT WORKS:
    - Extracts the salt from the hash
    - Hashes the plain password with that same salt
    - Compares the two hashes
    - Returns True if they match
    
    Args:
        plain_password: Password user just typed (e.g., "MyPassword123")
        hashed_password: Hash from database (e.g., "$2b$12$Eix...")
    
    Returns:
        True if password matches, False otherwise
    
    Example:
        >>> hashed = hash_password("SecurePass123")
        >>> verify_password("SecurePass123", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False

    """
    # pwd_context.verify() safely compares without revealing timing info
    # (constant-time comparison prevents timing attacks)
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """    
     WHAT IS A JWT TOKEN?
    - Like a special "pass" that proves user is logged in
    - Contains user info (email, expiration time)
    - Signed with SECRET_KEY (can't be faked!)
    - Has expiration time (old tokens stop working)
    
    Header.Payload.Signature
    - Header: Algorithm info (HS256)
    - Payload: User data (email, exp time)
    - Signature: Proves token hasn't been tampered with

    """
    # Make a copy of data (don't modify the original)
    to_encode = data.copy()
    if expires_delta:
        # Use custom expiration if provided
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Use default from settings (30 minutes)
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    
    # Create the JWT token
    # - to_encode: the data to put in the token
    # - settings.secret_key: secret key for signing
    # - algorithm: HS256 (HMAC with SHA-256)
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
     SECURITY CHECKS:
    - Signature verification (can't be faked)
    - Expiration check (old tokens rejected)
    - Algorithm verification (prevents algorithm confusion attacks)
    """
    try:
        # Decode the JWT token
        # - token: the token string to decode
        # - settings.secret_key: must match the key used to create it
        # - algorithms: only accept HS256 (prevents algorithm switching attacks)
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        # Extract email from token
        # "sub" is standard JWT claim for "subject" (the user identifier)
        email: Optional[str] = payload.get("sub")
        
        # If no email in token, it's invalid
        if email is None: 
            return None
        
        # Return TokenData with the email
        return TokenData(email=email)
        
    except JWTError:
        # Token is invalid (bad signature, expired, malformed, etc.)
        return None


