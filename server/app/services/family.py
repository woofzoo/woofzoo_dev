"""
Family service for business logic operations.

This module provides the FamilyService class for family-related business logic,
acting as an intermediary between controllers and repositories.
"""

from typing import List, Optional
import uuid

from app.models.family import Family
from app.repositories.family import FamilyRepository
from app.schemas.family import FamilyCreate, FamilyUpdate


class FamilyService:
    """
    Family service for business logic operations.
    
    This class handles business logic for family operations, including
    validation, business rules, and coordination between repositories.
    """
    
    def __init__(self, family_repository: FamilyRepository) -> None:
        """Initialize the family service."""
        self.family_repository = family_repository
    
    def create_family(self, family_data: FamilyCreate, owner_id: str) -> Family:
        """Create a new family with business logic validation."""
        # Convert owner_id string to UUID
        try:
            owner_id_uuid = uuid.UUID(owner_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid owner_id format: {owner_id}")
        
        # Create the family
        family = self.family_repository.create(
            name=family_data.name,
            description=family_data.description,
            owner_id=owner_id_uuid
        )
        
        return family
    
    def get_family_by_id(self, family_id: str) -> Optional[Family]:
        """Get a family by ID."""
        return self.family_repository.get_by_id(family_id)
    
    def get_families_by_owner(self, owner_id: str, skip: int = 0, limit: int = 100) -> List[Family]:
        """Get families by owner ID with pagination."""
        return self.family_repository.get_by_owner_id(owner_id, skip=skip, limit=limit)
    
    def update_family(self, family_id: str, family_data: FamilyUpdate) -> Optional[Family]:
        """Update a family with business logic validation."""
        # Check if family exists
        existing_family = self.family_repository.get_by_id(family_id)
        if not existing_family:
            return None
        
        # Prepare update data
        update_data = {}
        if family_data.name is not None:
            update_data["name"] = family_data.name
        if family_data.description is not None:
            update_data["description"] = family_data.description
        
        # Update the family
        return self.family_repository.update(family_id, **update_data)
    
    def delete_family(self, family_id: str) -> bool:
        """Delete a family."""
        return self.family_repository.delete(family_id)
    
    def search_families(self, search_term: str, owner_id: str = None, skip: int = 0, limit: int = 100) -> List[Family]:
        """Search families by name or description."""
        if not search_term.strip():
            if owner_id:
                return self.get_families_by_owner(owner_id, skip=skip, limit=limit)
            return []
        
        return self.family_repository.search_families(
            search_term=search_term.strip(),
            owner_id=owner_id,
            skip=skip,
            limit=limit
        )
    
    def get_family_count_by_owner(self, owner_id: str) -> int:
        """Get family count by owner ID."""
        return self.family_repository.count_by_owner(owner_id)
