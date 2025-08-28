"""
Owner service for business logic operations.

This module provides the OwnerService class for owner-related business logic,
acting as an intermediary between controllers and repositories.
"""

from typing import List, Optional

from app.models.owner import Owner
from app.repositories.owner import OwnerRepository
from app.schemas.owner import OwnerCreate, OwnerUpdate


class OwnerService:
    """
    Owner service for business logic operations.
    
    This class handles business logic for owner operations, including
    validation, business rules, and coordination between repositories.
    """
    
    def __init__(self, owner_repository: OwnerRepository) -> None:
        """Initialize the owner service."""
        self.owner_repository = owner_repository
    
    def create_owner(self, owner_data: OwnerCreate) -> Owner:
        """
        Create a new owner with business logic validation.
        
        Args:
            owner_data: Owner creation data
            
        Returns:
            Created owner instance
            
        Raises:
            ValueError: If owner with same phone number already exists
        """
        # Check if owner with same phone number already exists
        existing_owner = self.owner_repository.get_by_phone_number(owner_data.phone_number)
        if existing_owner:
            raise ValueError(f"Owner with phone number '{owner_data.phone_number}' already exists")
        
        # Create the owner
        owner = self.owner_repository.create(
            phone_number=owner_data.phone_number,
            name=owner_data.name,
            email=owner_data.email,
            address=owner_data.address
        )
        
        return owner
    
    def get_owner_by_id(self, owner_id: str) -> Optional[Owner]:
        """
        Get an owner by ID.
        
        Args:
            owner_id: Owner's ID
            
        Returns:
            Owner instance or None if not found
        """
        return self.owner_repository.get_by_id(owner_id)
    
    def get_owner_by_phone(self, phone_number: str) -> Optional[Owner]:
        """
        Get an owner by phone number.
        
        Args:
            phone_number: Owner's phone number
            
        Returns:
            Owner instance or None if not found
        """
        return self.owner_repository.get_by_phone_number(phone_number)
    
    def get_all_owners(self, skip: int = 0, limit: int = 100) -> List[Owner]:
        """
        Get all active owners with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active owner instances
        """
        return self.owner_repository.get_active_owners(skip=skip, limit=limit)
    
    def update_owner(self, owner_id: str, owner_data: OwnerUpdate) -> Optional[Owner]:
        """
        Update an owner with business logic validation.
        
        Args:
            owner_id: Owner's ID
            owner_data: Owner update data
            
        Returns:
            Updated owner instance or None if not found
        """
        # Check if owner exists
        existing_owner = self.owner_repository.get_by_id(owner_id)
        if not existing_owner:
            return None
        
        # Prepare update data
        update_data = {}
        if owner_data.name is not None:
            update_data["name"] = owner_data.name
        if owner_data.email is not None:
            update_data["email"] = owner_data.email
        if owner_data.address is not None:
            update_data["address"] = owner_data.address
        
        # Update the owner
        return self.owner_repository.update(owner_id, **update_data)
    
    def delete_owner(self, owner_id: str) -> bool:
        """
        Soft delete an owner (deactivate).
        
        Args:
            owner_id: Owner's ID
            
        Returns:
            True if deactivated, False if not found
        """
        return self.owner_repository.update(owner_id, is_active=False) is not None
    
    def search_owners(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Owner]:
        """
        Search owners by name or phone number.
        
        Args:
            search_term: Search term to match against name or phone
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching owner instances
        """
        return self.owner_repository.search_owners(
            search_term=search_term.strip(),
            skip=skip,
            limit=limit
        )
    
    def count_owners(self) -> int:
        """
        Get count of active owners.
        
        Returns:
            Number of active owners
        """
        return self.owner_repository.count_active_owners()
