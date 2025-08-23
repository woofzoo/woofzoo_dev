"""
Authentication controller for API layer.

This module provides the AuthController class for handling HTTP requests
and responses related to authentication operations.
"""

from typing import Optional

from fastapi import HTTPException, status

from app.schemas.auth import (
    UserSignup, UserLogin, PasswordResetRequest, PasswordReset, EmailVerification,
    LoginResponse, UserResponse, TokenResponse, MessageResponse, PersonalizationUpdate
)
from app.services.auth import AuthService
from app.services.jwt import JWTService


class AuthController:
    """
    Authentication controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to authentication operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, auth_service: AuthService, jwt_service: JWTService) -> None:
        """Initialize the authentication controller."""
        self.auth_service = auth_service
        self.jwt_service = jwt_service
    
    async def register_user(self, user_data: UserSignup) -> MessageResponse:
        """Register a new user."""
        try:
            user, email_sent = await self.auth_service.register_user(user_data)
            
            message = "User registered successfully"
            if not email_sent:
                message += ". However, verification email could not be sent. Please contact support."
            
            return MessageResponse(message=message)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register user"
            )
    
    async def login_user(self, login_data: UserLogin) -> LoginResponse:
        """Authenticate a user for login."""
        try:
            user = await self.auth_service.login_user(login_data)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Create tokens
            tokens = self.jwt_service.create_tokens_for_user(user)
            
            # Create response
            user_response = UserResponse.model_validate(user)
            token_response = TokenResponse(**tokens)
            
            return LoginResponse(user=user_response, tokens=token_response)
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to authenticate user"
            )
    
    async def verify_email(self, verification_data: EmailVerification) -> MessageResponse:
        """Verify user email address."""
        try:
            success = await self.auth_service.verify_email(verification_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired verification token"
                )
            
            return MessageResponse(message="Email verified successfully")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to verify email"
            )
    
    async def request_password_reset(self, reset_request: PasswordResetRequest) -> MessageResponse:
        """Request password reset for a user."""
        try:
            email_sent = await self.auth_service.request_password_reset(reset_request)
            
            # Always return success message for security (don't reveal if user exists)
            message = "If an account with that email exists, a password reset link has been sent"
            if not email_sent:
                message = "Password reset request processed"
            
            return MessageResponse(message=message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process password reset request"
            )
    
    async def reset_password(self, reset_data: PasswordReset) -> MessageResponse:
        """Reset user password using token."""
        try:
            success = await self.auth_service.reset_password(reset_data)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired reset token"
                )
            
            return MessageResponse(message="Password reset successfully")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to reset password"
            )
    
    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token."""
        try:
            tokens = await self.auth_service.refresh_tokens(refresh_token)
            if not tokens:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            return TokenResponse(**tokens)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to refresh tokens"
            )
    
    async def get_current_user(self, user_id: int) -> UserResponse:
        """Get current user information."""
        try:
            user = await self.auth_service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return UserResponse.model_validate(user)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get user information"
            )
    
    async def update_personalization(self, user_id: int, personalization_data: PersonalizationUpdate) -> UserResponse:
        """Update user personalization settings."""
        try:
            success = await self.auth_service.update_personalization(
                user_id, personalization_data.personalization
            )
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Get updated user
            user = await self.auth_service.get_user_by_id(user_id)
            return UserResponse.model_validate(user)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update personalization settings"
            )
    
    async def resend_verification_email(self, email: str) -> MessageResponse:
        """Resend verification email to user."""
        try:
            email_sent = await self.auth_service.resend_verification_email(email)
            
            # Always return success message for security
            message = "If an account with that email exists and is not verified, a verification email has been sent"
            if not email_sent:
                message = "Verification email request processed"
            
            return MessageResponse(message=message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to resend verification email"
            )
    
    async def change_password(self, user_id: int, current_password: str, new_password: str) -> MessageResponse:
        """Change user password."""
        try:
            success = await self.auth_service.change_password(user_id, current_password, new_password)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid current password or user not found"
                )
            
            return MessageResponse(message="Password changed successfully")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to change password"
            )
    
    async def logout(self, user_id: int) -> MessageResponse:
        """Logout user (client-side token invalidation)."""
        try:
            # In a more advanced implementation, you might want to blacklist the token
            # For now, we'll just return a success message
            return MessageResponse(message="Logged out successfully")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to logout"
            )
