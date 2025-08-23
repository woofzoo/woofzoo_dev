"""
JWT service for the application.

This module provides JWT token generation and validation functionality
for authentication and authorization.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
from jwt import PyJWTError

from app.config import settings
from app.models.user import User


class JWTService:
    """
    JWT service for token management.
    
    This class handles JWT token generation, validation, and refresh
    operations for user authentication.
    """
    
    def __init__(self) -> None:
        """Initialize the JWT service."""
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.refresh_token_expire_days = settings.refresh_token_expire_days
    
    def create_access_token(
        self,
        user_id: int,
        email: str,
        roles: list[str],
        personalization: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create an access token for a user.
        
        Args:
            user_id: User ID
            email: User email
            roles: User roles
            personalization: User personalization settings
            expires_delta: Optional custom expiration time
            
        Returns:
            str: JWT access token
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "roles": roles,
            "personalization": personalization,
            "type": "access",
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(
        self,
        user_id: int,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a refresh token for a user.
        
        Args:
            user_id: User ID
            expires_delta: Optional custom expiration time
            
        Returns:
            str: JWT refresh token
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        to_encode = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Optional[Dict[str, Any]]: Decoded token payload or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except PyJWTError:
            return None
    
    def verify_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode an access token.
        
        Args:
            token: JWT access token to verify
            
        Returns:
            Optional[Dict[str, Any]]: Decoded token payload or None if invalid
        """
        payload = self.verify_token(token)
        if payload and payload.get("type") == "access":
            return payload
        return None
    
    def verify_refresh_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a refresh token.
        
        Args:
            token: JWT refresh token to verify
            
        Returns:
            Optional[Dict[str, Any]]: Decoded token payload or None if invalid
        """
        payload = self.verify_token(token)
        if payload and payload.get("type") == "refresh":
            return payload
        return None
    
    def create_tokens_for_user(self, user: User) -> Dict[str, Any]:
        """
        Create both access and refresh tokens for a user.
        
        Args:
            user: User object
            
        Returns:
            Dict[str, Any]: Dictionary containing access and refresh tokens
        """
        access_token = self.create_access_token(
            user_id=user.id,
            email=user.email,
            roles=user.roles,
            personalization=user.personalization
        )
        
        refresh_token = self.create_refresh_token(user_id=user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60  # Convert to seconds
        }
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Create a new access token using a refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Optional[str]: New access token or None if refresh token is invalid
        """
        payload = self.verify_refresh_token(refresh_token)
        if not payload:
            return None
        
        user_id = int(payload.get("sub"))
        # Note: For a complete implementation, you would need to fetch user data
        # from the database here. This is a simplified version.
        return user_id
    
    def get_token_expiration(self, token: str) -> Optional[datetime]:
        """
        Get the expiration time of a token.
        
        Args:
            token: JWT token
            
        Returns:
            Optional[datetime]: Token expiration time or None if invalid
        """
        payload = self.verify_token(token)
        if payload and "exp" in payload:
            return datetime.fromtimestamp(payload["exp"])
        return None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Check if a token is expired.
        
        Args:
            token: JWT token
            
        Returns:
            bool: True if token is expired, False otherwise
        """
        expiration = self.get_token_expiration(token)
        if expiration:
            return datetime.utcnow() > expiration
        return True
