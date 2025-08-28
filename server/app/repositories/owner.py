"""
Owner repository for database operations.

This module provides the OwnerRepository class for owner-specific
database operations extending the base repository functionality.
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.owner import Owner
from app.repositories.base import BaseRepository


class OwnerRepository(BaseRepository[Owner]):
    """
    Owner repository for owner-specific database operations.
    
    This class extends BaseRepository to provide owner-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the owner repository."""
        super().__init__(Owner, session)
    
    def get_by_phone_number(self, phone_number: str) -> Optional[Owner]:
        """
        Get an owner by phone number.
        
        Args:
            phone_number: Owner's phone number
            
        Returns:
            Owner instance or None if not found
        """
        result = self.session.execute(
            select(Owner).where(Owner.phone_number == phone_number)
        )
        return result.scalar_one_or_none()
    
    def get_active_owners(self, skip: int = 0, limit: int = 100) -> list[Owner]:
        """
        Get all active owners with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active owner instances
        """
        result = self.session.execute(
            select(Owner)
            .where(Owner.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def search_owners(self, search_term: str, skip: int = 0, limit: int = 100) -> list[Owner]:
        """
        Search owners by name or phone number.
        
        Args:
            search_term: Search term to match against name or phone
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching owner instances
        """
        search_pattern = f"%{search_term}%"
        result = self.session.execute(
            select(Owner)
            .where(
                (Owner.name.ilike(search_pattern)) |
                (Owner.phone_number.ilike(search_pattern))
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def count_active_owners(self) -> int:
        """
        Get count of active owners.
        
        Returns:
            Number of active owners
        """
        result = self.session.execute(
            select(Owner).where(Owner.is_active == True)
        )
        return len(result.scalars().all())
