"""
Allergy Service for business logic operations.

This module provides the AllergyService class for allergy-related
business logic with access control.
"""

from typing import List, Optional
import uuid

from app.models.allergy import Allergy
from app.models.user import User
from app.repositories.allergy import AllergyRepository
from app.schemas.allergy import AllergyCreate, AllergyUpdate
from app.services.permission_service import PermissionService


class AllergyService:
    """
    Allergy service for business logic operations.
    
    This class handles business logic for allergy operations,
    including validation, access control, and coordination.
    """
    
    def __init__(
        self,
        allergy_repository: AllergyRepository,
        permission_service: PermissionService
    ):
        """Initialize the allergy service."""
        self.allergy_repository = allergy_repository
        self.permission_service = permission_service
    
    def create_allergy(
        self,
        allergy_data: AllergyCreate,
        current_user: User
    ) -> Optional[Allergy]:
        """
        Create a new allergy record with access control.
        
        Args:
            allergy_data: Allergy data
            current_user: User creating the allergy
            
        Returns:
            Created Allergy or None if unauthorized
        """
        # Check if user can create allergies for this pet
        if not self.permission_service.can_create_allergies(
            current_user,
            allergy_data.pet_id
        ):
            raise PermissionError("You don't have permission to add allergies for this pet")
        
        # Convert UUID strings
        try:
            pet_id_uuid = uuid.UUID(allergy_data.pet_id)
            doctor_id_uuid = uuid.UUID(allergy_data.diagnosed_by_doctor_id) if allergy_data.diagnosed_by_doctor_id else None
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {e}")
        
        # Create the allergy
        allergy = self.allergy_repository.create(
            pet_id=pet_id_uuid,
            allergen=allergy_data.allergen,
            allergy_type=allergy_data.allergy_type,
            severity=allergy_data.severity,
            symptoms=allergy_data.symptoms or {},
            reaction_description=allergy_data.reaction_description,
            diagnosed_by_doctor_id=doctor_id_uuid,
            diagnosed_date=allergy_data.diagnosed_date,
            notes=allergy_data.notes,
            is_active=True,
            created_by_user_id=current_user.public_id
        )
        
        return allergy
    
    def get_allergy(
        self,
        allergy_id: str,
        current_user: User
    ) -> Optional[Allergy]:
        """Get an allergy by ID with access control."""
        allergy = self.allergy_repository.get_by_id(allergy_id)
        
        if not allergy:
            return None
        
        if not self.permission_service.can_read_allergies(
            current_user,
            str(allergy.pet_id)
        ):
            raise PermissionError("You don't have permission to view this allergy")
        
        return allergy
    
    def get_allergies_by_pet(
        self,
        pet_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[Allergy]:
        """Get all allergies for a pet with access control."""
        if not self.permission_service.can_read_allergies(current_user, pet_id):
            raise PermissionError("You don't have permission to view allergies for this pet")
        
        return self.allergy_repository.get_by_pet_id(pet_id, skip=skip, limit=limit)
    
    def get_active_allergies(
        self,
        pet_id: str,
        current_user: User
    ) -> List[Allergy]:
        """Get active allergies for a pet."""
        if not self.permission_service.can_read_allergies(current_user, pet_id):
            raise PermissionError("You don't have permission to view allergies for this pet")
        
        return self.allergy_repository.get_active_allergies(pet_id)
    
    def get_critical_allergies(
        self,
        pet_id: str,
        current_user: User
    ) -> List[Allergy]:
        """Get critical (severe/life-threatening) allergies for a pet."""
        if not self.permission_service.can_read_allergies(current_user, pet_id):
            raise PermissionError("You don't have permission to view allergies for this pet")
        
        return self.allergy_repository.get_critical_allergies(pet_id)
    
    def update_allergy(
        self,
        allergy_id: str,
        allergy_data: AllergyUpdate,
        current_user: User
    ) -> Optional[Allergy]:
        """Update an allergy record."""
        existing = self.allergy_repository.get_by_id(allergy_id)
        
        if not existing:
            return None
        
        # Check if user can update allergies for this pet
        if not self.permission_service.can_create_allergies(
            current_user,
            str(existing.pet_id)
        ):
            raise PermissionError("You don't have permission to update allergies for this pet")
        
        # Prepare update data
        update_data = {}
        if allergy_data.severity is not None:
            update_data["severity"] = allergy_data.severity
        if allergy_data.symptoms is not None:
            update_data["symptoms"] = allergy_data.symptoms
        if allergy_data.reaction_description is not None:
            update_data["reaction_description"] = allergy_data.reaction_description
        if allergy_data.notes is not None:
            update_data["notes"] = allergy_data.notes
        if allergy_data.is_active is not None:
            update_data["is_active"] = allergy_data.is_active
        
        return self.allergy_repository.update(allergy_id, **update_data)

