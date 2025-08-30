"""
Family repository for database operations.

This module provides the FamilyRepository class for family-specific
database operations extending the base repository functionality.
"""

from typing import List, Optional
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.family import Family
from app.repositories.base import BaseRepository


class FamilyRepository(BaseRepository[Family]):
    """
    Family repository for family-specific database operations.
    
    This class extends BaseRepository to provide family-specific
    database operations and queries.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        """Initialize the family repository."""
        super().__init__(Family, session)
    
    def get_by_owner_id(self, owner_id: str, skip: int = 0, limit: int = 100) -> List[Family]:
        """Get families by owner ID."""
        try:
            owner_id_uuid = uuid.UUID(owner_id)
        except (ValueError, AttributeError):
            return []
        
        result = self.session.execute(
            select(Family)
            .where(Family.owner_id == owner_id_uuid)
            .where(Family.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def count_by_owner(self, owner_id: str) -> int:
        """Count families by owner ID."""
        try:
            owner_id_uuid = uuid.UUID(owner_id)
        except (ValueError, AttributeError):
            return 0
        
        result = self.session.execute(
            select(Family)
            .where(Family.owner_id == owner_id_uuid)
            .where(Family.is_active == True)
        )
        return len(result.scalars().all())
    
    def search_families(self, search_term: str, owner_id: str = None, skip: int = 0, limit: int = 100) -> List[Family]:
        """Search families by name or description."""
        search_pattern = f"%{search_term}%"
        query = select(Family).where(
            (Family.name.ilike(search_pattern)) |
            (Family.description.ilike(search_pattern))
        ).where(Family.is_active == True)
        
        if owner_id:
            try:
                owner_id_uuid = uuid.UUID(owner_id)
                query = query.where(Family.owner_id == owner_id_uuid)
            except (ValueError, AttributeError):
                return []
        
        result = self.session.execute(
            query.offset(skip).limit(limit)
        )
        return result.scalars().all()
