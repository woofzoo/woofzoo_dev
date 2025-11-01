"""
Pet Journal service for business logic operations.

This module provides the PetJournalService class for pet journal-related business logic,
acting as an intermediary between controllers and repositories.
"""

from datetime import date
from typing import List, Optional
import uuid

from app.models.pet_journal import PetJournal
from app.repositories.pet_journal_repository import PetJournalRepository
from app.repositories.pet import PetRepository
from app.schemas.pet_journal import PetJournalCreate, PetJournalUpdate
from loguru import logger


class PetJournalService:
    """
    Pet Journal service for business logic operations.
    
    This class handles business logic for pet journal operations, including
    validation, permissions, and coordination between repositories.
    """
    
    def __init__(
        self, 
        pet_journal_repository: PetJournalRepository,
        pet_repository: PetRepository
    ) -> None:
        """
        Initialize the pet journal service.
        
        Args:
            pet_journal_repository: Repository for pet journal operations
            pet_repository: Repository for pet operations
        """
        self.pet_journal_repository = pet_journal_repository
        self.pet_repository = pet_repository
    
    def create_journal_entry(
        self, 
        journal_data: PetJournalCreate,
        user_id: int
    ) -> PetJournal:
        """
        Create a new journal entry for a pet.
        
        Args:
            journal_data: Journal entry data
            user_id: ID of the user creating the entry
            
        Returns:
            Created journal entry
            
        Raises:
            ValueError: If pet not found or validation fails
        """
        # Convert pet_id string to UUID
        try:
            pet_id_uuid = uuid.UUID(journal_data.pet_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid pet_id format: {journal_data.pet_id}")
        
        # Verify pet exists
        pet = self.pet_repository.get_by_id(pet_id_uuid)
        if not pet:
            raise ValueError(f"Pet with ID {journal_data.pet_id} not found")
        
        # Create the journal entry
        entry = self.pet_journal_repository.create(
            pet_id=pet_id_uuid,
            created_by_user_id=user_id,
            entry_type=journal_data.entry_type,
            title=journal_data.title,
            content=journal_data.content,
            entry_date=journal_data.entry_date,
            metadata=journal_data.metadata or {}
        )
        
        logger.info(
            "Journal entry created",
            extra={
                "entry_id": str(entry.id),
                "pet_id": str(pet_id_uuid),
                "entry_type": journal_data.entry_type,
                "user_id": user_id
            }
        )
        
        return entry
    
    def get_journal_entry_by_id(self, entry_id: uuid.UUID) -> Optional[PetJournal]:
        """
        Get a journal entry by ID.
        
        Args:
            entry_id: Journal entry unique identifier
            
        Returns:
            Journal entry or None if not found
        """
        return self.pet_journal_repository.get_by_id(entry_id)
    
    def get_journal_entries_by_pet(
        self,
        pet_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        entry_type: Optional[str] = None
    ) -> List[PetJournal]:
        """
        Get journal entries for a pet with optional filtering.
        
        Args:
            pet_id: Pet's unique identifier
            skip: Number of records to skip
            limit: Maximum number of records to return
            entry_type: Optional filter by entry type
            
        Returns:
            List of journal entries
        """
        if entry_type:
            return self.pet_journal_repository.get_by_entry_type(
                pet_id, entry_type, skip, limit
            )
        return self.pet_journal_repository.get_by_pet_id(pet_id, skip, limit)
    
    def get_journal_entries_by_date_range(
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
            List of journal entries
        """
        return self.pet_journal_repository.get_by_date_range(
            pet_id, start_date, end_date, entry_type
        )
    
    def update_journal_entry(
        self,
        entry_id: uuid.UUID,
        update_data: PetJournalUpdate,
        user_id: int
    ) -> Optional[PetJournal]:
        """
        Update a journal entry.
        
        Args:
            entry_id: Journal entry unique identifier
            update_data: Update data
            user_id: ID of the user updating the entry
            
        Returns:
            Updated journal entry or None if not found
            
        Raises:
            ValueError: If user doesn't have permission to update
        """
        entry = self.pet_journal_repository.get_by_id(entry_id)
        if not entry:
            return None
        
        # Only allow the creator to update (can be extended for family members)
        if entry.created_by_user_id != user_id:
            raise ValueError("You don't have permission to update this journal entry")
        
        # Prepare update data
        update_dict = update_data.model_dump(exclude_unset=True)
        
        updated_entry = self.pet_journal_repository.update(entry_id, **update_dict)
        
        logger.info(
            "Journal entry updated",
            extra={
                "entry_id": str(entry_id),
                "user_id": user_id
            }
        )
        
        return updated_entry
    
    def delete_journal_entry(self, entry_id: uuid.UUID, user_id: int) -> bool:
        """
        Delete a journal entry.
        
        Args:
            entry_id: Journal entry unique identifier
            user_id: ID of the user deleting the entry
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If user doesn't have permission to delete
        """
        entry = self.pet_journal_repository.get_by_id(entry_id)
        if not entry:
            return False
        
        # Only allow the creator to delete (can be extended for family members)
        if entry.created_by_user_id != user_id:
            raise ValueError("You don't have permission to delete this journal entry")
        
        result = self.pet_journal_repository.delete(entry_id)
        
        if result:
            logger.info(
                "Journal entry deleted",
                extra={
                    "entry_id": str(entry_id),
                    "user_id": user_id
                }
            )
        
        return result
    
    def count_journal_entries(self, pet_id: uuid.UUID) -> int:
        """
        Count total journal entries for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            
        Returns:
            Total count of journal entries
        """
        return self.pet_journal_repository.count_by_pet_id(pet_id)

