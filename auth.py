from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

# Configuration constants
SECRET_KEY = "your_secret_key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security instance for token bearer authentication
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Payload to encode in the token
        expires_delta: Optional custom expiration time
        
    Returns:
        str: Encoded JWT token
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()
    
    # Set expiration time
    expire = datetime.utcnow() + (
        expires_delta if expires_delta 
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    
    # Create and return the encoded token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials) -> dict:
    """
    Verify and decode a JWT token
    
    Args:
        credentials: Token credentials to verify
        
    Returns:
        dict: Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Decode and verify the token
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
