from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from auth import verify_token
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling authentication across the application
    Validates JWT tokens for protected routes
    """
    
    # List of paths that don't require authentication
    PUBLIC_PATHS = {
        "/login",
        "/docs",
        "/openapi.json",
        "/redoc",
        "/static",
        "/users",
        "/dashboard",
        "/add-user",
        "/edit-users",
        "/manage-users",
    }

    async def dispatch(self, request: Request, call_next):
        """
        Process each request through the middleware
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware/route handler
            
        Returns:
            Response from the next handler
            
        Raises:
            HTTPException: If authentication fails
        """
        try:
            # Skip authentication for public paths
            if any(request.url.path.startswith(path) for path in self.PUBLIC_PATHS):
                return await call_next(request)
            
            # Get and validate authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise HTTPException(
                    status_code=401,
                    detail="No authorization header"
                )
            
            # Split and validate scheme
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication scheme"
                )
            
            # Verify token
            credentials = HTTPAuthorizationCredentials(
                scheme=scheme,
                credentials=token
            )
            verify_token(credentials)
            
            # Continue with the request
            return await call_next(request)
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail=str(e)
            )
