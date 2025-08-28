"""
Family Member repository for database operations.

This module provides the FamilyMemberRepository class for family member-specific
database operations extending the base repository functionality.
"""

from typing import List, Optional
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.family_member import FamilyMember
from app.repositories.base import BaseRepository


class FamilyMemberRepository(BaseRepository[FamilyMember]):
    """
    Family Member repository for family member-specific database operations.
    
    This class extends BaseRepository to provide family member-specific
    database operations and queries.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize the family member repository."""
        super().__init__(FamilyMember, session)
    
    def get_by_family_id(self, family_id: str, skip: int = 0, limit: int = 100) -> List[FamilyMember]:
        """Get family members by family ID."""
        try:
            family_id_uuid = uuid.UUID(family_id)
        except (ValueError, AttributeError):
            return []
        
        result = self.session.execute(
            select(FamilyMember)
            .where(FamilyMember.family_id == family_id_uuid)
            .where(FamilyMember.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[FamilyMember]:
        """Get family memberships by user ID."""
        try:
            user_id_uuid = uuid.UUID(user_id)
        except (ValueError, AttributeError):
            return []
        
        result = self.session.execute(
            select(FamilyMember)
            .where(FamilyMember.user_id == user_id_uuid)
            .where(FamilyMember.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_by_family_and_user(self, family_id: str, user_id: str) -> Optional[FamilyMember]:
        """Get family member by family ID and user ID."""
        try:
            family_id_uuid = uuid.UUID(family_id)
            user_id_uuid = uuid.UUID(user_id)
        except (ValueError, AttributeError):
            return None
        
        result = self.session.execute(
            select(FamilyMember)
            .where(FamilyMember.family_id == family_id_uuid)
            .where(FamilyMember.user_id == user_id_uuid)
            .where(FamilyMember.is_active == True)
        )
        return result.scalar_one_or_none()
    
    def count_by_family(self, family_id: str) -> int:
        """Count family members by family ID."""
        try:
            family_id_uuid = uuid.UUID(family_id)
        except (ValueError, AttributeError):
            return 0
        
        result = self.session.execute(
            select(FamilyMember)
            .where(FamilyMember.family_id == family_id_uuid)
            .where(FamilyMember.is_active == True)
        )
        return len(result.scalars().all())
    
    def count_by_user(self, user_id: str) -> int:
        """Count family memberships by user ID."""
        try:
            user_id_uuid = uuid.UUID(user_id)
        except (ValueError, AttributeError):
            return 0
        
        result = self.session.execute(
            select(FamilyMember)
            .where(FamilyMember.user_id == user_id_uuid)
            .where(FamilyMember.is_active == True)
        )
        return len(result.scalars().all())
