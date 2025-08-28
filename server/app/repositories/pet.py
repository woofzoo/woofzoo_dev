"""
Pet repository for database operations.

This module provides the PetRepository class for pet-specific
database operations extending the base repository functionality.
"""

from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pet import Pet
from app.repositories.base import BaseRepository


class PetRepository(BaseRepository[Pet]):
    """
    Pet repository for pet-specific database operations.
    
    This class extends BaseRepository to provide pet-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the pet repository."""
        super().__init__(Pet, session)
    
    def get_by_pet_id(self, pet_id: str) -> Optional[Pet]:
        """
        Get a pet by pet_id.
        
        Args:
            pet_id: Pet's unique identifier
            
        Returns:
            Pet instance or None if not found
        """
        result = self.session.execute(
            select(Pet).where(Pet.pet_id == pet_id)
        )
        return result.scalar_one_or_none()
    
    def get_by_owner_id(self, owner_id: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """
        Get all pets for a specific owner.
        
        Args:
            owner_id: Owner's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pet instances
        """
        result = self.session.execute(
            select(Pet)
            .where(Pet.owner_id == owner_id)
            .where(Pet.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def search_pets(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """
        Search pets by name, breed, or pet_type.
        
        Args:
            search_term: Search term to match against name, breed, or pet_type
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching pet instances
        """
        search_pattern = f"%{search_term}%"
        result = self.session.execute(
            select(Pet)
            .where(
                (Pet.name.ilike(search_pattern)) |
                (Pet.breed.ilike(search_pattern)) |
                (Pet.pet_type.ilike(search_pattern))
            )
            .where(Pet.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_by_pet_type(self, pet_type: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """
        Get all pets of a specific type.
        
        Args:
            pet_type: Type of pet (DOG, CAT, BIRD, etc.)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pet instances
        """
        result = self.session.execute(
            select(Pet)
            .where(Pet.pet_type == pet_type.upper())
            .where(Pet.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def get_by_breed(self, breed: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """
        Get all pets of a specific breed.
        
        Args:
            breed: Breed of pet
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pet instances
        """
        result = self.session.execute(
            select(Pet)
            .where(Pet.breed == breed)
            .where(Pet.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    def count_by_owner(self, owner_id: str) -> int:
        """
        Get count of pets for a specific owner.
        
        Args:
            owner_id: Owner's ID
            
        Returns:
            Number of pets owned by the owner
        """
        result = self.session.execute(
            select(Pet)
            .where(Pet.owner_id == owner_id)
            .where(Pet.is_active == True)
        )
        return len(result.scalars().all())
    
    def count_active_pets(self) -> int:
        """
        Get count of all active pets.
        
        Returns:
            Number of active pets
        """
        result = self.session.execute(
            select(Pet).where(Pet.is_active == True)
        )
        return len(result.scalars().all())
