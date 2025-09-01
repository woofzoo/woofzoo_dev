"""
Authentication middleware for route protection.

This module provides authentication middleware for protecting routes
and handling JWT token validation.
"""

from typing import Optional, List
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.services.jwt import JWTService
from app.repositories.user import UserRepository
from app.models.user import User

# Security scheme
security = HTTPBearer()


class AuthMiddleware:
    """
    Authentication middleware for route protection.
    
    This class provides methods for authenticating users and checking
    their permissions for accessing protected routes.
    """
    
    def __init__(self, jwt_service: JWTService, user_repository: UserRepository) -> None:
        """Initialize the authentication middleware."""
        self.jwt_service = jwt_service
        self.user_repository = user_repository
    
    def get_current_user_id(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
        """
        Get current user ID from JWT token.
        
        Args:
            credentials: HTTP authorization credentials
            
        Returns:
            User ID from token
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = self.jwt_service.verify_access_token(credentials.credentials)
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
        self, 
        user_id: int = Depends(lambda: AuthMiddleware.get_current_user_id),
        session: Session = Depends(get_db_session)
    ) -> User:
        """
        Get current user from database.
        
        Args:
            user_id: Current user ID
            session: Database session
            
        Returns:
            Current user object
            
        Raises:
            HTTPException: If user not found or inactive
        """
        user = self.user_repository.get_by_id(user_id)
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
    
    def require_roles(self, required_roles: List[str]):
        """
        Dependency factory to require specific roles.
        
        Args:
            required_roles: List of required roles
            
        Returns:
            Dependency function that checks user roles
        """
        def check_roles(current_user: User = Depends(lambda: AuthMiddleware.get_current_user)):
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
    
    def require_any_role(self, required_roles: List[str]):
        """
        Dependency factory to require any of the specified roles.
        
        Args:
            required_roles: List of required roles (user must have at least one)
            
        Returns:
            Dependency function that checks user roles
        """
        def check_any_role(current_user: User = Depends(lambda: AuthMiddleware.get_current_user)):
            """
            Check if current user has any of the required roles.
            
            Args:
                current_user: Current user object
                
            Returns:
                User: Current user if authorized
                
            Raises:
                HTTPException: If user doesn't have any required roles
            """
            user_roles = set(current_user.roles)
            required_roles_set = set(required_roles)
            
            if not user_roles.intersection(required_roles_set):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return current_user
        
        return check_any_role
    
    def require_all_roles(self, required_roles: List[str]):
        """
        Dependency factory to require all specified roles.
        
        Args:
            required_roles: List of required roles (user must have all)
            
        Returns:
            Dependency function that checks user roles
        """
        def check_all_roles(current_user: User = Depends(lambda: AuthMiddleware.get_current_user)):
            """
            Check if current user has all required roles.
            
            Args:
                current_user: Current user object
                
            Returns:
                User: Current user if authorized
                
            Raises:
                HTTPException: If user doesn't have all required roles
            """
            user_roles = set(current_user.roles)
            required_roles_set = set(required_roles)
            
            if not required_roles_set.issubset(user_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return current_user
        
        return check_all_roles
    
    def optional_auth(self, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[User]:
        """
        Optional authentication - returns user if authenticated, None otherwise.
        
        Args:
            credentials: Optional HTTP authorization credentials
            
        Returns:
            User object if authenticated, None otherwise
        """
        if not credentials:
            return None
        
        try:
            payload = self.jwt_service.verify_access_token(credentials.credentials)
            if payload is None:
                return None
            
            user_id = int(payload.get("sub"))
            if user_id is None:
                return None
            
            user = self.user_repository.get_by_id(user_id)
            if user is None or not user.is_active:
                return None
            
            return user
        except (ValueError, TypeError):
            return None
    
    def get_user_from_token(self, token: str) -> Optional[User]:
        """
        Get user from JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            User object if token is valid, None otherwise
        """
        try:
            payload = self.jwt_service.verify_access_token(token)
            if payload is None:
                return None
            
            user_id = int(payload.get("sub"))
            if user_id is None:
                return None
            
            user = self.user_repository.get_by_id(user_id)
            if user is None or not user.is_active:
                return None
            
            return user
        except (ValueError, TypeError):
            return None
    
    def validate_token(self, token: str) -> bool:
        """
        Validate JWT token.
        
        Args:
            token: JWT token to validate
            
        Returns:
            True if token is valid, False otherwise
        """
        payload = self.jwt_service.verify_access_token(token)
        return payload is not None
    
    def get_token_payload(self, token: str) -> Optional[dict]:
        """
        Get token payload without validation.
        
        Args:
            token: JWT token
            
        Returns:
            Token payload or None if invalid
        """
        return self.jwt_service.verify_access_token(token)
