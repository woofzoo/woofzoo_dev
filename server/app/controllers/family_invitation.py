"""
Family Invitation controller for API layer.

This module provides the FamilyInvitationController class for handling HTTP requests
and responses related to family invitation operations.
"""

from typing import List

from fastapi import HTTPException, status

from app.schemas.family import FamilyInvitationAccept, FamilyInvitationCreate, FamilyInvitationListResponse, FamilyInvitationResponse
from app.services.family_invitation import FamilyInvitationService


class FamilyInvitationController:
    """
    Family Invitation controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to family invitation operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, family_invitation_service: FamilyInvitationService) -> None:
        """Initialize the family invitation controller."""
        self.family_invitation_service = family_invitation_service
    
    def create_invitation(self, family_id: str, invitation_data: FamilyInvitationCreate, invited_by: str) -> FamilyInvitationResponse:
        """Create a new family invitation."""
        try:
            invitation = self.family_invitation_service.create_invitation(family_id, invitation_data, invited_by)
            return FamilyInvitationResponse.model_validate(invitation)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create invitation"
            )
    
    def get_invitation(self, invitation_id: str) -> FamilyInvitationResponse:
        """Get an invitation by ID."""
        invitation = self.family_invitation_service.get_invitation_by_id(invitation_id)
        if not invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invitation with ID {invitation_id} not found"
            )
        
        return FamilyInvitationResponse.model_validate(invitation)
    
    def get_family_invitations(self, family_id: str, skip: int = 0, limit: int = 100) -> FamilyInvitationListResponse:
        """Get family invitations by family ID with pagination."""
        try:
            invitations = self.family_invitation_service.get_family_invitations(family_id, skip=skip, limit=limit)
            total = self.family_invitation_service.get_invitation_count_by_family(family_id)
            
            invitation_responses = [FamilyInvitationResponse.model_validate(invitation) for invitation in invitations]
            return FamilyInvitationListResponse(invitations=invitation_responses, total=total)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve invitations"
            )
    
    def get_user_invitations(self, email: str, skip: int = 0, limit: int = 100) -> FamilyInvitationListResponse:
        """Get invitations by email with pagination."""
        try:
            invitations = self.family_invitation_service.get_user_invitations(email, skip=skip, limit=limit)
            
            invitation_responses = [FamilyInvitationResponse.model_validate(invitation) for invitation in invitations]
            return FamilyInvitationListResponse(invitations=invitation_responses, total=len(invitation_responses))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve user invitations"
            )
    
    def accept_invitation(self, token: str, user_id: str) -> dict:
        """Accept a family invitation."""
        try:
            success = self.family_invitation_service.accept_invitation(token, user_id)
            if success:
                return {"message": "Invitation accepted successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to accept invitation"
                )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to accept invitation"
            )
    
    def decline_invitation(self, token: str) -> dict:
        """Decline a family invitation."""
        try:
            success = self.family_invitation_service.decline_invitation(token)
            if success:
                return {"message": "Invitation declined successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to decline invitation"
                )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to decline invitation"
            )
    
    def cancel_invitation(self, invitation_id: str) -> dict:
        """Cancel a family invitation."""
        try:
            success = self.family_invitation_service.cancel_invitation(invitation_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Invitation with ID {invitation_id} not found"
                )
            
            return {"message": f"Invitation with ID {invitation_id} cancelled successfully"}
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to cancel invitation"
            )
    
    def resend_invitation(self, invitation_id: str) -> FamilyInvitationResponse:
        """Resend a family invitation."""
        try:
            invitation = self.family_invitation_service.resend_invitation(invitation_id)
            if not invitation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Invitation with ID {invitation_id} not found"
                )
            
            return FamilyInvitationResponse.model_validate(invitation)
        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to resend invitation"
            )
    
    def cleanup_expired_invitations(self) -> dict:
        """Clean up expired invitations."""
        try:
            cleaned_count = self.family_invitation_service.cleanup_expired_invitations()
            return {"message": f"Cleaned up {cleaned_count} expired invitations"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to cleanup expired invitations"
            )
