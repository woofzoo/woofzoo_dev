"""
Family Invitation service for business logic operations.

This module provides the FamilyInvitationService class for family invitation-related business logic,
acting as an intermediary between controllers and repositories.
"""

import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import List, Optional
import uuid

from app.models.family_invitation import FamilyInvitation
from app.repositories.family_invitation import FamilyInvitationRepository
from app.schemas.family import FamilyInvitationCreate
from app.config import settings


class FamilyInvitationService:
    """
    Family Invitation service for business logic operations.
    
    This class handles business logic for family invitation operations, including
    validation, business rules, and coordination between repositories.
    """
    
    def __init__(self, family_invitation_repository: FamilyInvitationRepository) -> None:
        """Initialize the family invitation service."""
        self.family_invitation_repository = family_invitation_repository
    
    def _generate_invitation_token(self) -> str:
        """Generate a secure invitation token."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(32))
    
    def create_invitation(self, family_id: str, invitation_data: FamilyInvitationCreate, invited_by: str) -> FamilyInvitation:
        """Create a new family invitation with business logic validation."""
        # Convert IDs to UUID
        try:
            family_id_uuid = uuid.UUID(family_id)
            invited_by_uuid = uuid.UUID(invited_by)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid ID format")
        
        # Check if invitation already exists for this email and family
        existing_invitation = self.family_invitation_repository.get_pending_by_email_and_family(
            invitation_data.email, family_id
        )
        if existing_invitation:
            raise ValueError(f"An invitation already exists for this email")
        
        # Generate invitation token
        token = self._generate_invitation_token()
        
        # Calculate expiration date
        expires_at = (datetime.now(timezone.utc) + timedelta(days=settings.family_invitation_expire_days)).replace(tzinfo=None)
        
        # Create the invitation
        invitation = self.family_invitation_repository.create(
            family_id=family_id_uuid,
            email=invitation_data.email,
            access_level=invitation_data.access_level,
            message=invitation_data.message,
            invited_by=invited_by_uuid,
            token=token,
            status="PENDING",
            expires_at=expires_at
        )
        
        return invitation
    
    def get_invitation_by_id(self, invitation_id: str) -> Optional[FamilyInvitation]:
        """Get an invitation by ID."""
        return self.family_invitation_repository.get_by_id(invitation_id)
    
    def get_invitation_by_token(self, token: str) -> Optional[FamilyInvitation]:
        """Get an invitation by token."""
        return self.family_invitation_repository.get_by_token(token)
    
    def get_family_invitations(self, family_id: str, skip: int = 0, limit: int = 100) -> List[FamilyInvitation]:
        """Get family invitations by family ID with pagination."""
        return self.family_invitation_repository.get_by_family_id(family_id, skip=skip, limit=limit)
    
    def get_user_invitations(self, email: str, skip: int = 0, limit: int = 100) -> List[FamilyInvitation]:
        """Get invitations by email with pagination."""
        return self.family_invitation_repository.get_by_email(email, skip=skip, limit=limit)
    
    def accept_invitation(self, token: str, user_id: str) -> bool:
        """Accept a family invitation."""
        # Get invitation by token
        invitation = self.family_invitation_repository.get_by_token(token)
        if not invitation:
            raise ValueError("Invalid invitation token")
        
        # Check if invitation is still pending
        if invitation.status != "PENDING":
            raise ValueError("Invitation has already been processed")
        
        # Check if invitation has expired
        if invitation.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
            raise ValueError("Invitation has expired")
        
        # Update invitation status
        self.family_invitation_repository.update(str(invitation.id), status="ACCEPTED")
        
        return True
    
    def decline_invitation(self, token: str) -> bool:
        """Decline a family invitation."""
        # Get invitation by token
        invitation = self.family_invitation_repository.get_by_token(token)
        if not invitation:
            raise ValueError("Invalid invitation token")
        
        # Check if invitation is still pending
        if invitation.status != "PENDING":
            raise ValueError("Invitation has already been processed")
        
        # Update invitation status
        self.family_invitation_repository.update(str(invitation.id), status="DECLINED")
        
        return True
    
    def cancel_invitation(self, invitation_id: str) -> bool:
        """Cancel a family invitation."""
        # Check if invitation exists
        invitation = self.family_invitation_repository.get_by_id(invitation_id)
        if not invitation:
            return False
        
        # Check if invitation is still pending
        if invitation.status != "PENDING":
            raise ValueError("Can only cancel pending invitations")
        
        # Update invitation status
        self.family_invitation_repository.update(invitation_id, status="CANCELLED")
        
        return True
    
    def resend_invitation(self, invitation_id: str) -> Optional[FamilyInvitation]:
        """Resend a family invitation."""
        # Get invitation
        invitation = self.family_invitation_repository.get_by_id(invitation_id)
        if not invitation:
            return None
        
        # Check if invitation is still pending
        if invitation.status != "PENDING":
            raise ValueError("Can only resend pending invitations")
        
        # Generate new token and expiration
        new_token = self._generate_invitation_token()
        new_expires_at = (datetime.now(timezone.utc) + timedelta(days=settings.family_invitation_expire_days)).replace(tzinfo=None)
        
        # Update invitation
        updated_invitation = self.family_invitation_repository.update(
            invitation_id,
            token=new_token,
            expires_at=new_expires_at
        )
        
        return updated_invitation
    
    def cleanup_expired_invitations(self) -> int:
        """Clean up expired invitations and return count of cleaned invitations."""
        expired_invitations = self.family_invitation_repository.get_expired_invitations()
        
        cleaned_count = 0
        for invitation in expired_invitations:
            if self.family_invitation_repository.update(str(invitation.id), status="EXPIRED"):
                cleaned_count += 1
        
        return cleaned_count
    
    def get_invitation_count_by_family(self, family_id: str) -> int:
        """Get invitation count by family ID."""
        return self.family_invitation_repository.count_by_family(family_id)
    
    def get_pending_invitation_count_by_email(self, email: str) -> int:
        """Get pending invitation count by email."""
        return self.family_invitation_repository.count_pending_by_email(email)
