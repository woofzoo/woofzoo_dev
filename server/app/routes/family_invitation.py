"""
Family Invitation routes for API endpoints.

This module defines all family invitation-related API endpoints with proper
dependency injection and request/response handling.
"""

from fastapi import APIRouter, Depends, Query, status

from app.controllers.family_invitation import FamilyInvitationController
from app.dependencies import get_family_invitation_controller
from app.schemas.family import FamilyInvitationAccept, FamilyInvitationCreate, FamilyInvitationListResponse, FamilyInvitationResponse

# Create router
router = APIRouter(prefix="/family-invitations", tags=["family-invitations"])


# API Endpoints
@router.post(
    "/",
    response_model=FamilyInvitationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a family invitation",
    description="Create a new invitation to join a family"
)
def create_invitation(
    family_id: str = Query(..., description="Family's unique identifier"),
    invited_by: str = Query(..., description="Inviter's unique identifier"),
    invitation_data: FamilyInvitationCreate = None,
    controller: FamilyInvitationController = Depends(get_family_invitation_controller)
) -> FamilyInvitationResponse:
    """Create a new family invitation."""
    return controller.create_invitation(family_id, invitation_data, invited_by)


@router.get(
    "/",
    response_model=FamilyInvitationListResponse,
    summary="Get family invitations",
    description="Retrieve invitations for a specific family with optional pagination"
)
def get_family_invitations(
    family_id: str = Query(..., description="Family's unique identifier"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: FamilyInvitationController = Depends(get_family_invitation_controller)
) -> FamilyInvitationListResponse:
    """Get family invitations by family ID with pagination."""
    return controller.get_family_invitations(family_id, skip=skip, limit=limit)


@router.get(
    "/user/{email}",
    response_model=FamilyInvitationListResponse,
    summary="Get user invitations",
    description="Retrieve all invitations for a specific email address"
)
def get_user_invitations(
    email: str,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    controller: FamilyInvitationController = Depends(get_family_invitation_controller)
) -> FamilyInvitationListResponse:
    """Get invitations by email with pagination."""
    return controller.get_user_invitations(email, skip=skip, limit=limit)


@router.get(
    "/{invitation_id}",
    response_model=FamilyInvitationResponse,
    summary="Get an invitation by ID",
    description="Retrieve a specific invitation by its ID"
)
def get_invitation(
    invitation_id: str,
    controller: FamilyInvitationController = Depends(get_family_invitation_controller)
) -> FamilyInvitationResponse:
    """Get an invitation by ID."""
    return controller.get_invitation(invitation_id)


@router.post(
    "/accept",
    summary="Accept an invitation",
    description="Accept a family invitation using the invitation token"
)
def accept_invitation(
    token: str = Query(..., description="Invitation token"),
    user_id: str = Query(..., description="User's unique identifier"),
    controller: FamilyInvitationController = Depends(get_family_invitation_controller)
) -> dict:
    """Accept a family invitation."""
    return controller.accept_invitation(token, user_id)


@router.post(
    "/decline",
    summary="Decline an invitation",
    description="Decline a family invitation using the invitation token"
)
def decline_invitation(
    token: str = Query(..., description="Invitation token"),
    controller: FamilyInvitationController = Depends(get_family_invitation_controller)
) -> dict:
    """Decline a family invitation."""
    return controller.decline_invitation(token)


@router.delete(
    "/{invitation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel an invitation",
    description="Cancel a family invitation by its ID"
)
def cancel_invitation(
    invitation_id: str,
    controller: FamilyInvitationController = Depends(get_family_invitation_controller)
) -> None:
    """Cancel a family invitation."""
    controller.cancel_invitation(invitation_id)


@router.post(
    "/{invitation_id}/resend",
    response_model=FamilyInvitationResponse,
    summary="Resend an invitation",
    description="Resend a family invitation with a new token and expiration"
)
def resend_invitation(
    invitation_id: str,
    controller: FamilyInvitationController = Depends(get_family_invitation_controller)
) -> FamilyInvitationResponse:
    """Resend a family invitation."""
    return controller.resend_invitation(invitation_id)


@router.post(
    "/cleanup",
    summary="Clean up expired invitations",
    description="Clean up expired invitations and return count of cleaned invitations"
)
def cleanup_expired_invitations(
    controller: FamilyInvitationController = Depends(get_family_invitation_controller)
) -> dict:
    """Clean up expired invitations."""
    return controller.cleanup_expired_invitations()
