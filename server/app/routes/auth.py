"""
Authentication routes for API endpoints.

This module defines all authentication-related API endpoints with proper
dependency injection and request/response handling.
"""

from fastapi import APIRouter, Depends, Query, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse

from app.controllers.auth import AuthController
from app.dependencies import get_auth_controller, get_current_user_id
from app.schemas.auth import (
    UserSignup, UserLogin, PasswordResetRequest, PasswordReset, EmailVerification,
    LoginResponse, UserResponse, TokenResponse, MessageResponse, PersonalizationUpdate
)

# Create router
router = APIRouter(prefix="/auth", tags=["authentication"])

# Security scheme
security = HTTPBearer()


# Public endpoints (no authentication required)
@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email verification"
)
def register_user(
    user_data: UserSignup,
    controller: AuthController = Depends(get_auth_controller)
) -> MessageResponse:
    """Register a new user."""
    return controller.register_user(user_data)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login user",
    description="Authenticate user and return access tokens"
)
def login_user(
    login_data: UserLogin,
    controller: AuthController = Depends(get_auth_controller)
) -> LoginResponse:
    """Login user."""
    return controller.login_user(login_data)


@router.post(
    "/verify-email",
    response_model=MessageResponse,
    summary="Verify email address",
    description="Verify user email address using verification token"
)
def verify_email(
    verification_data: EmailVerification,
    controller: AuthController = Depends(get_auth_controller)
) -> MessageResponse:
    """Verify user email address."""
    return controller.verify_email(verification_data)


@router.get(
    "/verify-email",
    summary="Verify email address via GET",
    description="Verify user email address using verification token from email link"
)
def verify_email_get(
    token: str = Query(..., description="Email verification token"),
    controller: AuthController = Depends(get_auth_controller)
):
    """
    Verify email address via GET request (for email links).
    
    This endpoint is designed to be called directly from email verification links.
    It will verify the email and redirect to the frontend with a success message.
    """
    try:
        # Verify the email
        success = controller.verify_email(EmailVerification(token=token))
        
        if success:
            # Redirect to frontend with success message
            redirect_url = f"{controller.auth_service.email_service.frontend_url}/email-verified?status=success"
            return RedirectResponse(url=redirect_url, status_code=302)
        else:
            # Redirect to frontend with error message
            redirect_url = f"{controller.auth_service.email_service.frontend_url}/email-verified?status=error&message=invalid_token"
            return RedirectResponse(url=redirect_url, status_code=302)
            
    except Exception as e:
        # Redirect to frontend with error message
        redirect_url = f"{controller.auth_service.email_service.frontend_url}/email-verified?status=error&message=verification_failed"
        return RedirectResponse(url=redirect_url, status_code=302)


@router.post(
    "/request-password-reset",
    response_model=MessageResponse,
    summary="Request password reset",
    description="Send password reset email to user"
)
def request_password_reset(
    reset_request: PasswordResetRequest,
    controller: AuthController = Depends(get_auth_controller)
) -> MessageResponse:
    """Request password reset."""
    return controller.request_password_reset(reset_request)


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Reset password",
    description="Reset user password using reset token"
)
def reset_password(
    reset_data: PasswordReset,
    controller: AuthController = Depends(get_auth_controller)
) -> MessageResponse:
    """Reset user password."""
    return controller.reset_password(reset_data)


@router.get(
    "/reset-password",
    summary="Show password reset form",
    description="Show password reset form for token from email link"
)
async def reset_password_get(
    token: str = Query(..., description="Password reset token"),
    controller: AuthController = Depends(get_auth_controller)
):
    """
    Show password reset form via GET request (for email links).
    
    This endpoint is designed to be called directly from password reset email links.
    It will redirect to the frontend password reset form with the token.
    """
    # Validate token exists (don't verify expiration here, let the form handle it)
    user = await controller.auth_service.user_repository.get_by_reset_token(token)
    
    if user:
        # Token exists, redirect to frontend reset form
        redirect_url = f"{controller.auth_service.email_service.frontend_url}/reset-password?token={token}"
        return RedirectResponse(url=redirect_url, status_code=302)
    else:
        # Invalid token, redirect to frontend with error
        redirect_url = f"{controller.auth_service.email_service.frontend_url}/reset-password?status=error&message=invalid_token"
        return RedirectResponse(url=redirect_url, status_code=302)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Get new access token using refresh token"
)
def refresh_tokens(
    refresh_token: str = Query(..., description="Refresh token"),
    controller: AuthController = Depends(get_auth_controller)
) -> TokenResponse:
    """Refresh access token."""
    return controller.refresh_tokens(refresh_token)


@router.post(
    "/resend-verification",
    response_model=MessageResponse,
    summary="Resend verification email",
    description="Resend email verification link to user"
)
def resend_verification_email(
    email: str = Query(..., description="User email address"),
    controller: AuthController = Depends(get_auth_controller)
) -> MessageResponse:
    """Resend verification email."""
    return controller.resend_verification_email(email)


# Protected endpoints (authentication required)
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get current authenticated user information"
)
def get_current_user(
    user_id: int = Depends(get_current_user_id),
    controller: AuthController = Depends(get_auth_controller)
) -> UserResponse:
    """Get current user information."""
    return controller.get_current_user(user_id)


@router.put(
    "/me/personalization",
    response_model=UserResponse,
    summary="Update personalization settings",
    description="Update current user's personalization settings"
)
def update_personalization(
    personalization_data: PersonalizationUpdate,
    user_id: int = Depends(get_current_user_id),
    controller: AuthController = Depends(get_auth_controller)
) -> UserResponse:
    """Update user personalization settings."""
    return controller.update_personalization(user_id, personalization_data)


@router.post(
    "/me/change-password",
    response_model=MessageResponse,
    summary="Change password",
    description="Change current user's password"
)
def change_password(
    current_password: str = Query(..., description="Current password"),
    new_password: str = Query(..., description="New password"),
    user_id: int = Depends(get_current_user_id),
    controller: AuthController = Depends(get_auth_controller)
) -> MessageResponse:
    """Change user password."""
    return controller.change_password(user_id, current_password, new_password)


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout user",
    description="Logout current user (client-side token invalidation)"
)
def logout(
    user_id: int = Depends(get_current_user_id),
    controller: AuthController = Depends(get_auth_controller)
) -> MessageResponse:
    """Logout user."""
    return controller.logout(user_id)


# Health check endpoint
@router.get(
    "/health",
    response_model=MessageResponse,
    summary="Authentication service health check",
    description="Check if authentication service is running"
)
async def health_check() -> MessageResponse:
    """Health check endpoint."""
    return MessageResponse(message="Authentication service is running")
