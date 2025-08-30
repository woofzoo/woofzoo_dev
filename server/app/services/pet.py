"""
Pet service for business logic operations.

This module provides the PetService class for pet-related business logic,
acting as an intermediary between controllers and repositories.
"""

import uuid
from typing import List, Optional

from app.models.pet import Pet
from app.repositories.pet import PetRepository
from app.schemas.pet import PetCreate, PetUpdate


class PetService:
    """
    Pet service for business logic operations.
    
    This class handles business logic for pet operations, including
    validation, business rules, and coordination between repositories.
    """
    
    def __init__(self, pet_repository: PetRepository, pet_id_service) -> None:
        """Initialize the pet service."""
        self.pet_repository = pet_repository
        self.pet_id_service = pet_id_service
    
    def create_pet(self, pet_data: PetCreate) -> Pet:
        """Create a new pet with business logic validation."""
        # Convert owner_id string to UUID
        try:
            owner_id_uuid = uuid.UUID(pet_data.owner_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid owner_id format: {pet_data.owner_id}")
        
        # Generate unique pet ID
        pet_id = self.pet_id_service.generate_pet_id(pet_data.pet_type, pet_data.breed)
        
        # Create the pet
        pet = self.pet_repository.create(
            pet_id=pet_id,
            owner_id=owner_id_uuid,
            name=pet_data.name,
            pet_type=pet_data.pet_type,
            breed=pet_data.breed,
            age=pet_data.age,
            gender=pet_data.gender,
            weight=pet_data.weight,
            photos=pet_data.photos or [],
            emergency_contacts=pet_data.emergency_contacts or {},
            insurance_info=pet_data.insurance_info or {}
        )
        
        return pet
    
    def get_pet_by_id(self, pet_id: str) -> Optional[Pet]:
        """Get a pet by ID."""
        return self.pet_repository.get_by_id(pet_id)
    
    def get_pet_by_pet_id(self, pet_id: str) -> Optional[Pet]:
        """Get a pet by pet_id."""
        return self.pet_repository.get_by_pet_id(pet_id)
    
    def get_pets_by_owner(self, owner_id: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """Get all pets for a specific owner."""
        return self.pet_repository.get_by_owner_id(owner_id, skip=skip, limit=limit)
    
    def update_pet(self, pet_id: str, pet_data: PetUpdate) -> Optional[Pet]:
        """Update a pet with business logic validation."""
        # Check if pet exists
        existing_pet = self.pet_repository.get_by_id(pet_id)
        if not existing_pet:
            return None
        
        # Prepare update data
        update_data = {}
        if pet_data.name is not None:
            update_data["name"] = pet_data.name
        if pet_data.pet_type is not None:
            update_data["pet_type"] = pet_data.pet_type
        if pet_data.breed is not None:
            update_data["breed"] = pet_data.breed
        if pet_data.age is not None:
            update_data["age"] = pet_data.age
        if pet_data.gender is not None:
            update_data["gender"] = pet_data.gender
        if pet_data.weight is not None:
            update_data["weight"] = pet_data.weight
        if pet_data.photos is not None:
            update_data["photos"] = pet_data.photos
        if pet_data.emergency_contacts is not None:
            update_data["emergency_contacts"] = pet_data.emergency_contacts
        if pet_data.insurance_info is not None:
            update_data["insurance_info"] = pet_data.insurance_info
        
        # Update the pet
        return self.pet_repository.update(pet_id, **update_data)
    
    def delete_pet(self, pet_id: str) -> bool:
        """Delete a pet (soft delete)."""
        return self.pet_repository.delete(pet_id)
    
    def search_pets(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """Search pets by name or breed."""
        if not search_term.strip():
            return self.pet_repository.get_all(skip=skip, limit=limit)
        
        return self.pet_repository.search_pets(
            search_term=search_term.strip(),
            skip=skip,
            limit=limit
        )
    
    def get_pets_by_type(self, pet_type: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """Get pets by type."""
        return self.pet_repository.get_by_pet_type(pet_type, skip=skip, limit=limit)
    
    def get_pets_by_breed(self, breed: str, skip: int = 0, limit: int = 100) -> List[Pet]:
        """Get pets by breed."""
        return self.pet_repository.get_by_breed(breed, skip=skip, limit=limit)
    
    def count_pets_by_owner(self, owner_id: str) -> int:
        """Count pets for a specific owner."""
        return self.pet_repository.count_by_owner(owner_id)
    
    def count_active_pets(self) -> int:
        """Count all active pets."""
        return self.pet_repository.count_active_pets()
    
    def lookup_pet(self, pet_id: str) -> Optional[Pet]:
        """Lookup a pet by pet_id."""
        return self.pet_repository.get_by_pet_id(pet_id)

