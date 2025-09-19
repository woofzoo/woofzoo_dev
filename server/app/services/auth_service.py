"""
Authentication service for user authentication and authorization.

This module provides the AuthenticationService class for handling
user authentication, registration, and token management.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext

from app.models.user import User
from app.repositories.user import UserRepository
from app.services.jwt import JWTService
from app.services.email import EmailService
from app.schemas.auth import UserSignup, UserLogin, PasswordResetRequest

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:
    """
    Authentication service for user authentication and authorization.
    
    This class handles user registration, login, password management,
    and token operations.
    """
    
    def __init__(
        self, 
        user_repository: UserRepository, 
        jwt_service: JWTService,
        email_service: EmailService
    ) -> None:
        """Initialize the authentication service."""
        self.user_repository = user_repository
        self.jwt_service = jwt_service
        self.email_service = email_service
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """
        Hash a password.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return pwd_context.hash(password)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.user_repository.get_by_email(email)
        if not user:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def register_user(self, user_data: UserSignup) -> User:
        """
        Register a new user.
        
        Args:
            user_data: User registration data
            
        Returns:
            Created user object
            
        Raises:
            ValueError: If email already exists or validation fails
        """
        # Check if email already exists
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Hash password
        hashed_password = self.get_password_hash(user_data.password)
        
        # Create user
        user = self.user_repository.create(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            roles=user_data.roles,
            personalization=user_data.personalization
        )
        
        return user
    
    def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """
        Login a user and return tokens.
        
        Args:
            login_data: User login data
            
        Returns:
            Dictionary with tokens and user info
            
        Raises:
            ValueError: If authentication fails
        """
        user = self.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise ValueError("Invalid email or password")
        
        # Update last login
        self.user_repository.update(user.id, last_login=datetime.now(timezone.utc).replace(tzinfo=None))
        
        # Create tokens
        tokens = self.jwt_service.create_token_pair(
            user_id=user.id,
            email=user.email,
            roles=user.roles
        )
        
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": "bearer",
            "expires_in": self.jwt_service.access_token_expire_minutes * 60,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "roles": user.roles,
                "personalization": user.personalization
            }
        }
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Dictionary with new access token
            
        Raises:
            ValueError: If refresh token is invalid
        """
        new_access_token = self.jwt_service.refresh_access_token(refresh_token)
        if not new_access_token:
            raise ValueError("Invalid refresh token")
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": self.jwt_service.access_token_expire_minutes * 60
        }
    
    def request_password_reset(self, email: str) -> bool:
        """
        Request password reset for a user.
        
        Args:
            email: User email
            
        Returns:
            True if reset email sent, False if user not found
        """
        user = self.user_repository.get_by_email(email)
        if not user:
            return False
        
        # Generate reset token
        reset_token = self.jwt_service.create_access_token(
            {"sub": str(user.id), "type": "password_reset"},
            expires_delta=timedelta(minutes=30)  # 30 minutes expiry
        )
        
        # Update user with reset token
        self.user_repository.update(
            user.id,
            password_reset_token=reset_token,
            password_reset_expires=(datetime.now(timezone.utc) + timedelta(minutes=30)).replace(tzinfo=None)
        )
        
        # Send reset email
        try:
            self.email_service.send_password_reset_email(user.email, reset_token)
            return True
        except Exception:
            return False
    
    def reset_password(self, reset_token: str, new_password: str) -> bool:
        """
        Reset user password using reset token.
        
        Args:
            reset_token: Password reset token
            new_password: New password
            
        Returns:
            True if password reset successful, False otherwise
        """
        # Verify reset token
        payload = self.jwt_service.verify_access_token(reset_token)
        if not payload or payload.get("type") != "password_reset":
            return False
        
        user_id = int(payload.get("sub"))
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False
        
        # Check if token matches and is not expired
        if user.password_reset_token != reset_token:
            return False
        
        if user.password_reset_expires and user.password_reset_expires < datetime.now(timezone.utc).replace(tzinfo=None):
            return False
        
        # Hash new password
        hashed_password = self.get_password_hash(new_password)
        
        # Update user password and clear reset token
        self.user_repository.update(
            user.id,
            password_hash=hashed_password,
            password_reset_token=None,
            password_reset_expires=None
        )
        
        return True
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            True if password change successful, False otherwise
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False
        
        # Verify current password
        if not self.verify_password(current_password, user.password_hash):
            return False
        
        # Hash new password
        hashed_password = self.get_password_hash(new_password)
        
        # Update password
        self.user_repository.update(user.id, password_hash=hashed_password)
        
        return True
    
    def verify_email(self, verification_token: str) -> bool:
        """
        Verify user email using verification token.
        
        Args:
            verification_token: Email verification token
            
        Returns:
            True if email verification successful, False otherwise
        """
        # Verify token
        payload = self.jwt_service.verify_access_token(verification_token)
        if not payload or payload.get("type") != "email_verification":
            return False
        
        user_id = int(payload.get("sub"))
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False
        
        # Check if token matches and is not expired
        if user.email_verification_token != verification_token:
            return False
        
        if user.email_verification_expires and user.email_verification_expires < datetime.now(timezone.utc).replace(tzinfo=None):
            return False
        
        # Mark email as verified
        self.user_repository.update(
            user.id,
            is_verified=True,
            email_verification_token=None,
            email_verification_expires=None
        )
        
        return True
    
    def send_verification_email(self, user_id: int) -> bool:
        """
        Send email verification to user.
        
        Args:
            user_id: User ID
            
        Returns:
            True if verification email sent, False otherwise
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False
        
        # Generate verification token
        verification_token = self.jwt_service.create_access_token(
            {"sub": str(user.id), "type": "email_verification"},
            expires_delta=timedelta(hours=24)  # 24 hours expiry
        )
        
        # Update user with verification token
        self.user_repository.update(
            user.id,
            email_verification_token=verification_token,
            email_verification_expires=(datetime.now(timezone.utc) + timedelta(hours=24)).replace(tzinfo=None)
        )
        
        # Send verification email
        try:
            self.email_service.send_verification_email(user.email, verification_token)
            return True
        except Exception:
            return False
    
    def get_user_by_token(self, token: str) -> Optional[User]:
        """
        Get user from JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            User object if token is valid, None otherwise
        """
        payload = self.jwt_service.verify_access_token(token)
        if not payload:
            return None
        
        user_id = int(payload.get("sub"))
        user = self.user_repository.get_by_id(user_id)
        
        if not user or not user.is_active:
            return None
        
        return user
    
    def logout_user(self, user_id: int) -> bool:
        """
        Logout a user (invalidate tokens).
        
        Args:
            user_id: User ID
            
        Returns:
            True if logout successful, False otherwise
        """
        # In a more sophisticated implementation, you might want to:
        # 1. Add tokens to a blacklist
        # 2. Update user's last logout time
        # 3. Clear any session data
        
        # For now, we'll just return True as JWT tokens are stateless
        return True
