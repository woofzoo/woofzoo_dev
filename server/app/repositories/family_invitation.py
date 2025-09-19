"""
Family Invitation repository for database operations.

This module provides the FamilyInvitationRepository class for family invitation-specific
database operations extending the base repository functionality.
"""

from typing import List, Optional
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.family_invitation import FamilyInvitation
from app.repositories.base import BaseRepository


class FamilyInvitationRepository(BaseRepository[FamilyInvitation]):
    """
    Family Invitation repository for family invitation-specific database operations.
    
    This class extends BaseRepository to provide family invitation-specific
    database operations and queries.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize the family invitation repository."""
        super().__init__(FamilyInvitation, session)
    
    def get_by_family_id(self, family_id: str, skip: int = 0, limit: int = 100) -> List[FamilyInvitation]:
        """Get family invitations by family ID."""
        try:
            family_id_uuid = uuid.UUID(family_id)
        except (ValueError, AttributeError):
            return []
        
        result = self.session.execute(
            select(FamilyInvitation)
            .where(FamilyInvitation.family_id == family_id_uuid)
            .where(FamilyInvitation.is_active == True)
            .order_by(FamilyInvitation.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_by_email(self, email: str, skip: int = 0, limit: int = 100) -> List[FamilyInvitation]:
        """Get family invitations by email."""
        result = self.session.execute(
            select(FamilyInvitation)
            .where(FamilyInvitation.email == email)
            .where(FamilyInvitation.is_active == True)
            .order_by(FamilyInvitation.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_by_token(self, token: str) -> Optional[FamilyInvitation]:
        """Get family invitation by token."""
        result = self.session.execute(
            select(FamilyInvitation)
            .where(FamilyInvitation.token == token)
            .where(FamilyInvitation.is_active == True)
        )
        return result.scalar_one_or_none()
    
    def get_pending_by_email_and_family(self, email: str, family_id: str) -> Optional[FamilyInvitation]:
        """Get pending invitation by email and family ID."""
        try:
            family_id_uuid = uuid.UUID(family_id)
        except (ValueError, AttributeError):
            return None
        
        result = self.session.execute(
            select(FamilyInvitation)
            .where(FamilyInvitation.email == email)
            .where(FamilyInvitation.family_id == family_id_uuid)
            .where(FamilyInvitation.status == "PENDING")
            .where(FamilyInvitation.is_active == True)
        )
        return result.scalar_one_or_none()
    
    def get_expired_invitations(self) -> List[FamilyInvitation]:
        """Get expired invitations."""
        current_time = datetime.now(timezone.utc).replace(tzinfo=None)
        result = self.session.execute(
            select(FamilyInvitation)
            .where(FamilyInvitation.expires_at < current_time)
            .where(FamilyInvitation.status == "PENDING")
            .where(FamilyInvitation.is_active == True)
        )
        return result.scalars().all()
    
    def count_by_family(self, family_id: str) -> int:
        """Count family invitations by family ID."""
        try:
            family_id_uuid = uuid.UUID(family_id)
        except (ValueError, AttributeError):
            return 0
        
        result = self.session.execute(
            select(FamilyInvitation)
            .where(FamilyInvitation.family_id == family_id_uuid)
            .where(FamilyInvitation.is_active == True)
        )
        return len(result.scalars().all())
    
    def count_pending_by_email(self, email: str) -> int:
        """Count pending invitations by email."""
        result = self.session.execute(
            select(FamilyInvitation)
            .where(FamilyInvitation.email == email)
            .where(FamilyInvitation.status == "PENDING")
            .where(FamilyInvitation.is_active == True)
        )
        return len(result.scalars().all())
