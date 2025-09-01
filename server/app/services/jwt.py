"""
JWT service for token management.

This module provides the JWTService class for generating and validating
JWT tokens for authentication and authorization.
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, DecodeError

from app.config import settings


class JWTService:
    """
    JWT service for token management.
    
    This class handles JWT token generation, validation, and management
    for authentication and authorization purposes.
    """
    
    def __init__(self) -> None:
        """Initialize the JWT service."""
        self.secret_key = settings.secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.refresh_token_expire_days = settings.refresh_token_expire_days
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create an access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Optional custom expiration time
            
        Returns:
            Encoded JWT access token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a refresh token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Optional custom expiration time
            
        Returns:
            Encoded JWT refresh token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Decoded token payload or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except (InvalidTokenError, ExpiredSignatureError, DecodeError):
            return None
    
    def verify_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode an access token.
        
        Args:
            token: JWT access token to verify
            
        Returns:
            Decoded token payload or None if invalid
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
            Decoded token payload or None if invalid
        """
        payload = self.verify_token(token)
        if payload and payload.get("type") == "refresh":
            return payload
        return None
    
    def create_token_pair(self, user_id: int, email: str, roles: list[str]) -> Dict[str, str]:
        """
        Create both access and refresh tokens.
        
        Args:
            user_id: User ID
            email: User email
            roles: User roles
            
        Returns:
            Dictionary with access_token and refresh_token
        """
        access_token_data = {
            "sub": str(user_id),
            "email": email,
            "roles": roles
        }
        
        refresh_token_data = {
            "sub": str(user_id),
            "email": email
        }
        
        access_token = self.create_access_token(access_token_data)
        refresh_token = self.create_refresh_token(refresh_token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Create a new access token using a refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access token or None if refresh token is invalid
        """
        payload = self.verify_refresh_token(refresh_token)
        if not payload:
            return None
        
        # Create new access token with same user data
        access_token_data = {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "roles": payload.get("roles", [])
        }
        
        return self.create_access_token(access_token_data)
    
    def get_token_expiration(self, token: str) -> Optional[datetime]:
        """
        Get token expiration time.
        
        Args:
            token: JWT token
            
        Returns:
            Expiration datetime or None if token is invalid
        """
        payload = self.verify_token(token)
        if payload and "exp" in payload:
            return datetime.fromtimestamp(payload["exp"])
        return None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired.
        
        Args:
            token: JWT token
            
        Returns:
            True if token is expired, False otherwise
        """
        payload = self.verify_token(token)
        if not payload:
            return True
        
        exp_timestamp = payload.get("exp")
        if not exp_timestamp:
            return True
        
        return datetime.utcnow() > datetime.fromtimestamp(exp_timestamp)
