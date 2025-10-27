"""
Authentication Logic - Password hashing and JWT tokens

🎯 YOUR MISSION (Week 2):
Implement secure authentication functions

📚 LEARNING RESOURCES:
- Password Hashing: https://www.youtube.com/watch?v=cczlpiiu42M
- JWT Tokens: https://jwt.io/introduction
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

💡 KEY CONCEPTS:
- Never store plain passwords!
- Hash passwords with bcrypt (one-way encryption)
- Use JWT tokens for stateless authentication
- Tokens expire for security
"""

# TODO: Import necessary modules
# HINT: from passlib.context import CryptContext
# HINT: from datetime import datetime, timedelta
# HINT: from jose import JWTError, jwt
# HINT: from app.config import settings


# TODO: Create password context for hashing
# HINT: pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO: Function to hash passwords
# HINT: def get_password_hash(password: str) -> str:
# HINT:     return pwd_context.hash(password)


# TODO: Function to verify passwords
# HINT: def verify_password(plain_password: str, hashed_password: str) -> bool:
# HINT:     return pwd_context.verify(plain_password, hashed_password)


# TODO: Function to create access token
# HINT: def create_access_token(data: dict) -> str:
# HINT:     to_encode = data.copy()
# HINT:     expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
# HINT:     to_encode.update({"exp": expire})
# HINT:     encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
# HINT:     return encoded_jwt


# TODO: Function to decode and verify token
# HINT: def verify_token(token: str) -> dict:
# HINT:     try:
# HINT:         payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
# HINT:         return payload
# HINT:     except JWTError:
# HINT:         return None


# 📖 UNDERSTANDING THE CODE:
# 
# Password Hashing (bcrypt):
# - Input: "mypassword123"
# - Output: "$2b$12$KIXxZq3..."  (random, irreversible)
# - Same password → different hash each time (salt)
# - Verify by hashing input and comparing
#
# JWT Tokens:
# - Header: Algorithm info
# - Payload: User data (email, id, etc.)
# - Signature: Proves token wasn't tampered with
# - Server creates and verifies tokens
# - Client stores token and sends with each request
#
# Token Flow:
# 1. User logs in with email/password
# 2. Server verifies password
# 3. Server creates JWT token
# 4. Client stores token (localStorage/cookie)
# 5. Client sends token with each request
# 6. Server verifies token and identifies user

# 🎯 CHALLENGE:
# Add functions for:
# - Refresh tokens (longer expiry)
# - Token blacklist (logout functionality)
# - Password reset tokens

# ⚠️ SECURITY NOTES:
# - SECRET_KEY must be random and secret!
# - Use HTTPS in production
# - Set appropriate token expiry times
# - Never log passwords or tokens

# 🧪 TESTING:
# password = "test123"
# hashed = get_password_hash(password)
# print(verify_password("test123", hashed))  # True
# print(verify_password("wrong", hashed))     # False

