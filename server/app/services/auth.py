"""
Authentication service for the application.

This module provides the AuthService class for authentication-related business logic,
including user registration, login, password reset, and email verification.
"""

import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from passlib.context import CryptContext

from app.models.user import User
from app.repositories.user import UserRepository
from app.services.email import EmailService
from app.services.jwt import JWTService
from app.schemas.auth import UserSignup, UserLogin, PasswordResetRequest, PasswordReset, EmailVerification
from app.config import settings
from loguru import logger


class AuthService:
    """
    Authentication service for business logic operations.
    
    This class handles business logic for authentication operations, including
    user registration, login, password reset, and email verification.
    """
    
    def __init__(self, user_repository: UserRepository, email_service: EmailService, jwt_service: JWTService) -> None:
        """Initialize the authentication service."""
        self.user_repository = user_repository
        self.email_service = email_service
        self.jwt_service = jwt_service
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        return self.pwd_context.hash(password)
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def _generate_token(self) -> str:
        """Generate a secure random token."""
        return secrets.token_urlsafe(32)
    
    def register_user(self, user_data: UserSignup) -> Tuple[User, bool]:
        """
        Register a new user.
        
        Args:
            user_data: User signup data
            
        Returns:
            Tuple[User, bool]: Created user and email sent status
        """
        # Check if user with email already exists
        existing_user = self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"User with email '{user_data.email}' already exists")
        
        # Check if user with phone already exists (if phone is provided)
        if user_data.phone:
            existing_phone_user = self.user_repository.get_by_phone(user_data.phone)
            if existing_phone_user:
                raise ValueError(f"User with phone number '{user_data.phone}' already exists")
        
        # Hash password
        hashed_password = self._hash_password(user_data.password)
        
        # Generate verification token
        verification_token = self._generate_token()
        verification_expires = datetime.now(timezone.utc) + timedelta(hours=settings.email_verification_expire_hours)
        
        # Create user
        user = self.user_repository.create(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            roles=user_data.roles,
            email_verification_token=verification_token,
            email_verification_expires=verification_expires,
            personalization={},  # Default empty personalization
            is_verified=settings.auto_verify_users  # Auto-verify in development mode
        )
        
        # Send verification email (skip if auto-verify is enabled)
        if settings.auto_verify_users:
            email_sent = True  # Skip email sending in development mode
        else:
            email_sent = self.email_service.send_verification_email(
                to_email=user.email,
                to_name=user.full_name,
                token=verification_token
            )
        
        return user, email_sent
    
    def login_user(self, login_data: UserLogin) -> Optional[User]:
        """
        Authenticate a user for login.
        
        Args:
            login_data: User login data
            
        Returns:
            Optional[User]: Authenticated user or None
        """
        # Get user by email
        user = self.user_repository.get_by_email(login_data.email)
        if not user:
            return None
        
        # Verify password
        if not self._verify_password(login_data.password, user.password_hash):
            return None
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("Account is deactivated")
        
        # Update last login
        self.user_repository.update_last_login(user.id)
        
        return user
    
    def verify_email(self, verification_data: EmailVerification) -> bool:
        """
        Verify user email address.
        
        Args:
            verification_data: Email verification data
            
        Returns:
            bool: True if verification successful, False otherwise
        """
        logger.debug(
            "Starting email verification for token prefix={token_prefix}",
            token_prefix=verification_data.token[:10],
        )
        
        # Get user by verification token
        user = self.user_repository.get_by_verification_token(verification_data.token)
        if not user:
            logger.debug(
                "No user found with verification token prefix={token_prefix}",
                token_prefix=verification_data.token[:10],
            )
            return False
        
        logger.debug("Found user email={email} id={id}", email=user.email, id=user.id)
        logger.debug("User verification status {status}", status=user.is_verified)
        logger.debug("Token expires at {expires}", expires=user.email_verification_expires)
        logger.debug("Current time {now}", now=datetime.now(timezone.utc))
        
        # Check if token is expired
        if user.email_verification_expires and user.email_verification_expires.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            logger.debug("Token expired at {expires}", expires=user.email_verification_expires)
            return False
        
        logger.debug("Token is valid, proceeding with verification")
        
        # Clear verification token and mark as verified
        success = self.user_repository.clear_verification_token(user.id)
        
        if success:
            logger.debug("Successfully cleared verification token and marked user as verified")
            # Send welcome email
            self.email_service.send_welcome_email(
                to_email=user.email,
                to_name=user.full_name
            )
            logger.debug("Welcome email sent to {email}", email=user.email)
        else:
            logger.error("Failed to clear verification token")
        
        return success
    
    def request_password_reset(self, reset_request: PasswordResetRequest) -> bool:
        """
        Request password reset for a user.
        
        Args:
            reset_request: Password reset request data
            
        Returns:
            bool: True if reset email sent successfully, False otherwise
        """
        # Get user by email
        user = self.user_repository.get_by_email(reset_request.email)
        if not user:
            # Don't reveal if user exists or not for security
            return True
        
        # Generate reset token
        reset_token = self._generate_token()
        reset_expires = datetime.now(timezone.utc) + timedelta(hours=settings.password_reset_expire_hours)
        
        # Update user with reset token
        self.user_repository.update_reset_token(
            user_id=user.id,
            token=reset_token,
            expires_at=reset_expires
        )
        
        # Send password reset email
        email_sent = self.email_service.send_password_reset_email(
            to_email=user.email,
            to_name=user.full_name,
            token=reset_token
        )
        
        return email_sent
    
    def reset_password(self, reset_data: PasswordReset) -> bool:
        """
        Reset user password using token.
        
        Args:
            reset_data: Password reset data
            
        Returns:
            bool: True if password reset successful, False otherwise
        """
        # Get user by reset token
        user = self.user_repository.get_by_reset_token(reset_data.token)
        if not user:
            return False
        
        # Check if token is expired
        if user.password_reset_expires and user.password_reset_expires.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return False
        
        # Hash new password
        hashed_password = self._hash_password(reset_data.new_password)
        
        # Update password and clear reset token
        success = self.user_repository.update(
            user.id,
            password_hash=hashed_password
        )
        
        if success:
            self.user_repository.clear_reset_token(user.id)
        
        return success
    
    def refresh_tokens(self, refresh_token: str) -> Optional[dict]:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            Optional[dict]: New tokens or None if invalid
        """
        # Verify refresh token
        payload = self.jwt_service.verify_refresh_token(refresh_token)
        if not payload:
            return None
        
        # Get user
        user_id = int(payload.get("sub"))
        user = self.user_repository.get_by_id(user_id)
        if not user or not user.is_active:
            return None
        
        # Create new tokens
        tokens = self.jwt_service.create_tokens_for_user(user)
        return tokens
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.user_repository.get_by_id(user_id)
    
    def update_personalization(self, user_id: int, personalization: dict) -> bool:
        """
        Update user personalization settings.
        
        Args:
            user_id: User ID
            personalization: Personalization settings
            
        Returns:
            bool: True if update successful, False otherwise
        """
        return self.user_repository.update_personalization(user_id, personalization)
    
    def resend_verification_email(self, email: str) -> bool:
        """
        Resend verification email to user.
        
        Args:
            email: User email address
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        # Get user by email
        user = self.user_repository.get_by_email(email)
        if not user or user.is_verified:
            return False
        
        # Generate new verification token
        verification_token = self._generate_token()
        verification_expires = datetime.now(timezone.utc) + timedelta(hours=settings.email_verification_expire_hours)
        
        # Update verification token
        self.user_repository.update_verification_token(
            user_id=user.id,
            token=verification_token,
            expires_at=verification_expires
        )
        
        # Send verification email
        email_sent = self.email_service.send_verification_email(
            to_email=user.email,
            to_name=user.full_name,
            token=verification_token
        )
        
        return email_sent
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            bool: True if password changed successfully, False otherwise
        """
        # Get user
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False
        
        # Verify current password
        if not self._verify_password(current_password, user.password_hash):
            return False
        
        # Hash new password
        hashed_password = self._hash_password(new_password)
        
        # Update password
        success = self.user_repository.update(
            user.id,
            password_hash=hashed_password
        )
        
        return success
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate a user account.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if deactivation successful, False otherwise
        """
        return self.user_repository.update(user_id, is_active=False)
    
    def activate_user(self, user_id: int) -> bool:
        """
        Activate a user account.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if activation successful, False otherwise
        """
        return self.user_repository.update(user_id, is_active=True)
