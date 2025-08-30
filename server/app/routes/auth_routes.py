"""
Authentication routes for API endpoints.

This module defines all authentication-related API endpoints with proper
dependency injection and request/response handling.
"""

from fastapi import APIRouter, Depends, status

from app.controllers.auth_controller import AuthenticationController
from app.dependencies import get_auth_controller, get_current_user_id
from app.schemas.auth import UserSignup, UserLogin, PasswordResetRequest, RefreshTokenRequest

# Create router
router = APIRouter(prefix="/auth", tags=["authentication"])


# API Endpoints
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with the provided data"
)
def register_user(
    user_data: UserSignup,
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Register a new user."""
    return controller.register_user(user_data)


@router.post(
    "/login",
    summary="Login user",
    description="Authenticate user and return access tokens"
)
def login_user(
    login_data: UserLogin,
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Login a user."""
    return controller.login_user(login_data)


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Get a new access token using refresh token"
)
def refresh_token(
    refresh_data: RefreshTokenRequest,
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Refresh access token."""
    return controller.refresh_token(refresh_data)


@router.post(
    "/logout",
    summary="Logout user",
    description="Logout user and invalidate tokens"
)
def logout_user(
    user_id: int = Depends(get_current_user_id),
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Logout a user."""
    return controller.logout_user(user_id)


@router.post(
    "/password-reset-request",
    summary="Request password reset",
    description="Send password reset email to user"
)
def request_password_reset(
    reset_data: PasswordResetRequest,
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Request password reset."""
    return controller.request_password_reset(reset_data)


@router.post(
    "/password-reset",
    summary="Reset password",
    description="Reset password using reset token"
)
def reset_password(
    reset_token: str,
    new_password: str,
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Reset password using reset token."""
    return controller.reset_password(reset_token, new_password)


@router.post(
    "/change-password",
    summary="Change password",
    description="Change user password (requires authentication)"
)
def change_password(
    current_password: str,
    new_password: str,
    user_id: int = Depends(get_current_user_id),
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Change user password."""
    return controller.change_password(user_id, current_password, new_password)


@router.post(
    "/verify-email",
    summary="Verify email",
    description="Verify user email using verification token"
)
def verify_email(
    verification_token: str,
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Verify user email."""
    return controller.verify_email(verification_token)


@router.post(
    "/send-verification-email",
    summary="Send verification email",
    description="Send email verification to user (requires authentication)"
)
def send_verification_email(
    user_id: int = Depends(get_current_user_id),
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Send verification email."""
    return controller.send_verification_email(user_id)


@router.get(
    "/me",
    summary="Get current user",
    description="Get current user information (requires authentication)"
)
def get_current_user(
    user_id: int = Depends(get_current_user_id),
    controller: AuthenticationController = Depends(get_auth_controller)
) -> dict:
    """Get current user information."""
    return controller.get_current_user(user_id)
