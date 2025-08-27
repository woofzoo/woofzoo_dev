"""
Dependency injection configuration for the application.

This module centralizes all dependency injection functions for the current project.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.services.email import EmailService
from app.services.jwt import JWTService
from app.controllers.auth import AuthController

# Security scheme
security = HTTPBearer()


# =============================================================================
# DATABASE DEPENDENCIES
# =============================================================================

def get_user_repository(session: Session = Depends(get_db_session)) -> UserRepository:
    """
    Dependency to get user repository.
    
    Args:
        session: Database session
        
    Returns:
        UserRepository instance
    """
    return UserRepository(session)


# =============================================================================
# SERVICE DEPENDENCIES
# =============================================================================

def get_email_service() -> EmailService:
    """
    Dependency to get email service.
    
    Returns:
        EmailService instance
    """
    return EmailService()


def get_jwt_service() -> JWTService:
    """
    Dependency to get JWT service.
    
    Returns:
        JWTService instance
    """
    return JWTService()


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    email_service: EmailService = Depends(get_email_service),
    jwt_service: JWTService = Depends(get_jwt_service)
) -> AuthService:
    """
    Dependency to get authentication service.
    
    Args:
        user_repository: User repository instance
        email_service: Email service instance
        jwt_service: JWT service instance
        
    Returns:
        AuthService instance
    """
    return AuthService(user_repository, email_service, jwt_service)


# =============================================================================
# CONTROLLER DEPENDENCIES
# =============================================================================

def get_auth_controller(
    auth_service: AuthService = Depends(get_auth_service),
    jwt_service: JWTService = Depends(get_jwt_service)
) -> AuthController:
    """
    Dependency to get authentication controller.
    
    Args:
        auth_service: Authentication service instance
        jwt_service: JWT service instance
        
    Returns:
        AuthController instance
    """
    return AuthController(auth_service, jwt_service)


# =============================================================================
# AUTHENTICATION DEPENDENCIES
# =============================================================================

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service)
) -> int:
    """
    Get current user ID from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        jwt_service: JWT service instance
        
    Returns:
        int: User ID
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt_service.verify_access_token(credentials.credentials)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user_id
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    user_id: int = Depends(get_current_user_id),
    user_repository: UserRepository = Depends(get_user_repository)
):
    """
    Get current user from database.
    
    Args:
        user_id: Current user ID
        user_repository: User repository instance
        
    Returns:
        User: Current user object
        
    Raises:
        HTTPException: If user not found or inactive
    """
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def require_roles(required_roles: list[str]):
    """
    Dependency factory to require specific roles.
    
    Args:
        required_roles: List of required roles
        
    Returns:
        Dependency function that checks user roles
    """
    def check_roles(
        current_user = Depends(get_current_user)
    ):
        """
        Check if current user has required roles.
        
        Args:
            current_user: Current user object
            
        Returns:
            User: Current user if authorized
            
        Raises:
            HTTPException: If user doesn't have required roles
        """
        user_roles = set(current_user.roles)
        required_roles_set = set(required_roles)
        
        if not user_roles.intersection(required_roles_set):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        
        return current_user
    
    return check_roles
