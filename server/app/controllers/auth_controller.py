"""
Authentication controller for API layer.

This module provides the AuthenticationController class for handling HTTP requests
and responses related to authentication operations.
"""

from typing import Dict, Any

from fastapi import HTTPException, status

from app.schemas.auth import UserSignup, UserLogin, PasswordResetRequest, RefreshTokenRequest
from app.services.auth_service import AuthenticationService
from loguru import logger


class AuthenticationController:
    """
    Authentication controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to authentication operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, auth_service: AuthenticationService) -> None:
        """Initialize the authentication controller."""
        self.auth_service = auth_service
    
    def register_user(self, user_data: UserSignup) -> Dict[str, Any]:
        """Register a new user."""
        try:
            user = self.auth_service.register_user(user_data)
            return {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "roles": user.roles,
                    "is_verified": user.is_verified
                }
            }
        except ValueError as e:
            logger.warning("User registration failed: {message}", message=str(e))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error during user registration")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to register user"
            )
    
    def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Login a user."""
        try:
            result = self.auth_service.login_user(login_data)
            return result
        except ValueError as e:
            logger.warning("Login failed: {message}", message=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error during login")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to login user"
            )
    
    def refresh_token(self, refresh_data: RefreshTokenRequest) -> Dict[str, Any]:
        """Refresh access token."""
        try:
            result = self.auth_service.refresh_access_token(refresh_data.refresh_token)
            return result
        except ValueError as e:
            logger.warning("Token refresh failed: {message}", message=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error during token refresh")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to refresh token"
            )
    
    def request_password_reset(self, reset_data: PasswordResetRequest) -> Dict[str, str]:
        """Request password reset."""
        try:
            success = self.auth_service.request_password_reset(reset_data.email)
            if success:
                return {"message": "Password reset email sent successfully"}
            else:
                # Don't reveal if email exists or not for security
                return {"message": "If the email exists, a password reset link has been sent"}
        except Exception as e:
            logger.exception("Unexpected error while requesting password reset")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send password reset email"
            )
    
    def reset_password(self, reset_token: str, new_password: str) -> Dict[str, str]:
        """Reset password using reset token."""
        try:
            success = self.auth_service.reset_password(reset_token, new_password)
            if success:
                return {"message": "Password reset successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired reset token"
                )
        except HTTPException:
            # Error already mapped to user; log the message only
            logger.error("Password reset failed: Invalid or expired reset token")
            raise
        except Exception as e:
            logger.exception("Unexpected error during password reset")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to reset password"
            )
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> Dict[str, str]:
        """Change user password."""
        try:
            success = self.auth_service.change_password(user_id, current_password, new_password)
            if success:
                return {"message": "Password changed successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid current password"
                )
        except HTTPException:
            logger.error("Change password failed: Invalid current password")
            raise
        except Exception as e:
            logger.exception("Unexpected error during change password")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to change password"
            )
    
    def verify_email(self, verification_token: str) -> Dict[str, str]:
        """Verify user email."""
        try:
            success = self.auth_service.verify_email(verification_token)
            if success:
                return {"message": "Email verified successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired verification token"
                )
        except HTTPException:
            logger.error("Email verification failed: Invalid or expired verification token")
            raise
        except Exception as e:
            logger.exception("Unexpected error during email verification")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to verify email"
            )
    
    def send_verification_email(self, user_id: int) -> Dict[str, str]:
        """Send verification email."""
        try:
            success = self.auth_service.send_verification_email(user_id)
            if success:
                return {"message": "Verification email sent successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to send verification email"
                )
        except HTTPException:
            logger.error("Send verification email failed: user state invalid")
            raise
        except Exception as e:
            logger.exception("Unexpected error sending verification email")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send verification email"
            )
    
    def logout_user(self, user_id: int) -> Dict[str, str]:
        """Logout a user."""
        try:
            success = self.auth_service.logout_user(user_id)
            if success:
                return {"message": "Logged out successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to logout"
                )
        except HTTPException:
            logger.error("Logout failed: user state invalid")
            raise
        except Exception as e:
            logger.exception("Unexpected error during logout")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to logout"
            )
    
    def get_current_user(self, user_id: int) -> Dict[str, Any]:
        """Get current user information."""
        try:
            user = self.auth_service.get_user_by_token(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            return {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "roles": user.roles,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "personalization": user.personalization,
                "last_login": user.last_login.isoformat() if user.last_login else None,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        except HTTPException:
            logger.error("Get current user failed: user not found")
            raise
        except Exception as e:
            logger.exception("Unexpected error getting current user")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get user information"
            )
