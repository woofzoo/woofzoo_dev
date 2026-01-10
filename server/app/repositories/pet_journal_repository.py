"""
Pet Journal repository for database operations.

This module provides the PetJournalRepository class for managing
pet journal entries in the database.
"""

from datetime import date
from typing import List, Optional
import uuid

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models.pet_journal import PetJournal
from app.repositories.base import BaseRepository


class PetJournalRepository(BaseRepository[PetJournal]):
    """
    Repository for pet journal database operations.
    
    This class provides database access methods for pet journal entries.
    """
    
    def __init__(self, session: Session) -> None:
        """
        Initialize the pet journal repository.
        
        Args:
            session: Database session
        """
        super().__init__(PetJournal, session)
    
    def get_by_pet_id(
        self,
        pet_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[PetJournal]:
        """
        Get all journal entries for a pet with pagination.
        
        Args:
            pet_id: Pet's unique identifier
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pet journal entries
        """
        stmt = (
            select(PetJournal)
            .where(PetJournal.pet_id == pet_id)
            .order_by(PetJournal.entry_date.desc(), PetJournal.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def get_by_entry_type(
        self,
        pet_id: uuid.UUID,
        entry_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[PetJournal]:
        """
        Get journal entries by type for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            entry_type: Type of journal entry
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pet journal entries
        """
        stmt = (
            select(PetJournal)
            .where(
                and_(
                    PetJournal.pet_id == pet_id,
                    PetJournal.entry_type == entry_type
                )
            )
            .order_by(PetJournal.entry_date.desc(), PetJournal.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def get_by_date_range(
        self,
        pet_id: uuid.UUID,
        start_date: date,
        end_date: date,
        entry_type: Optional[str] = None
    ) -> List[PetJournal]:
        """
        Get journal entries within a date range.
        
        Args:
            pet_id: Pet's unique identifier
            start_date: Start date of range (inclusive)
            end_date: End date of range (inclusive)
            entry_type: Optional filter by entry type
            
        Returns:
            List of pet journal entries
        """
        conditions = [
            PetJournal.pet_id == pet_id,
            PetJournal.entry_date >= start_date,
            PetJournal.entry_date <= end_date
        ]
        
        if entry_type:
            conditions.append(PetJournal.entry_type == entry_type)
        
        stmt = (
            select(PetJournal)
            .where(and_(*conditions))
            .order_by(PetJournal.entry_date.desc(), PetJournal.created_at.desc())
        )
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def count_by_pet_id(self, pet_id: uuid.UUID) -> int:
        """
        Count total journal entries for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            
        Returns:
            Total count of journal entries
        """
        stmt = select(PetJournal).where(PetJournal.pet_id == pet_id)
        result = self.session.execute(stmt)
        return len(list(result.scalars().all()))
    
    def update(self, journal_id: uuid.UUID, **kwargs) -> Optional[PetJournal]:
        """
        Update a journal entry.
        
        Args:
            journal_id: Journal entry unique identifier
            **kwargs: Fields to update
            
        Returns:
            Updated journal entry or None if not found
        """
        entry = self.get_by_id(journal_id)
        if not entry:
            return None
        
        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
        
        return self.update_entity(entry)
    
    def delete(self, journal_id: uuid.UUID) -> bool:
        """
        Delete a journal entry.
        
        Args:
            journal_id: Journal entry unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        entry = self.get_by_id(journal_id)
        if not entry:
            return False
        
        self.delete_entity(entry)
        return True

