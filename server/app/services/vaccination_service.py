"""
Vaccination Service for business logic operations.

This module provides the VaccinationService class for vaccination-related
business logic with access control.
"""

from typing import List, Optional
from datetime import date, timedelta
import uuid

from app.models.vaccination import Vaccination
from app.models.user import User
from app.repositories.vaccination import VaccinationRepository
from app.schemas.vaccination import VaccinationCreate, VaccinationUpdate
from app.services.permission_service import PermissionService


class VaccinationService:
    """
    Vaccination service for business logic operations.
    
    This class handles business logic for vaccination operations,
    including validation, access control, and coordination.
    """
    
    def __init__(
        self,
        vaccination_repository: VaccinationRepository,
        permission_service: PermissionService
    ):
        """Initialize the vaccination service."""
        self.vaccination_repository = vaccination_repository
        self.permission_service = permission_service
    
    def create_vaccination(
        self,
        vaccination_data: VaccinationCreate,
        current_user: User
    ) -> Optional[Vaccination]:
        """
        Create a new vaccination record with access control.
        
        Args:
            vaccination_data: Vaccination data
            current_user: User creating the vaccination
            
        Returns:
            Created Vaccination or None if unauthorized
        """
        # Only doctors can create vaccination records
        if not self.permission_service.can_create_vaccinations(
            current_user,
            vaccination_data.pet_id
        ):
            raise PermissionError("Only doctors can create vaccination records")
        
        # Convert UUID strings
        try:
            pet_id_uuid = uuid.UUID(vaccination_data.pet_id)
            doctor_id_uuid = uuid.UUID(vaccination_data.administered_by_doctor_id)
            clinic_id_uuid = uuid.UUID(vaccination_data.clinic_id)
            medical_record_id_uuid = uuid.UUID(vaccination_data.medical_record_id) if vaccination_data.medical_record_id else None
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {e}")
        
        # Create the vaccination
        vaccination = self.vaccination_repository.create(
            pet_id=pet_id_uuid,
            medical_record_id=medical_record_id_uuid,
            vaccine_name=vaccination_data.vaccine_name,
            vaccine_type=vaccination_data.vaccine_type,
            manufacturer=vaccination_data.manufacturer,
            batch_number=vaccination_data.batch_number,
            administered_by_doctor_id=doctor_id_uuid,
            administered_at=vaccination_data.administered_at,
            administration_site=vaccination_data.administration_site,
            clinic_id=clinic_id_uuid,
            next_due_date=vaccination_data.next_due_date,
            is_booster=vaccination_data.is_booster,
            reaction_notes=vaccination_data.reaction_notes,
            certificate_url=vaccination_data.certificate_url,
            is_required_by_law=vaccination_data.is_required_by_law
        )
        
        return vaccination
    
    def get_vaccination(
        self,
        vaccination_id: str,
        current_user: User
    ) -> Optional[Vaccination]:
        """Get a vaccination by ID with access control."""
        vaccination = self.vaccination_repository.get_by_id(vaccination_id)
        
        if not vaccination:
            return None
        
        if not self.permission_service.can_read_vaccinations(
            current_user,
            str(vaccination.pet_id)
        ):
            raise PermissionError("You don't have permission to view this vaccination")
        
        return vaccination
    
    def get_vaccinations_by_pet(
        self,
        pet_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[Vaccination]:
        """Get all vaccinations for a pet with access control."""
        if not self.permission_service.can_read_vaccinations(current_user, pet_id):
            raise PermissionError("You don't have permission to view vaccinations for this pet")
        
        return self.vaccination_repository.get_by_pet_id(pet_id, skip=skip, limit=limit)
    
    def get_due_vaccinations(
        self,
        pet_id: str,
        current_user: User
    ) -> List[Vaccination]:
        """Get vaccinations that are due or overdue for a pet."""
        if not self.permission_service.can_read_vaccinations(current_user, pet_id):
            raise PermissionError("You don't have permission to view vaccinations for this pet")
        
        return self.vaccination_repository.get_due_vaccinations(pet_id)
    
    def get_upcoming_vaccinations(
        self,
        pet_id: str,
        current_user: User,
        days: int = 30
    ) -> List[Vaccination]:
        """Get vaccinations due within specified days."""
        if not self.permission_service.can_read_vaccinations(current_user, pet_id):
            raise PermissionError("You don't have permission to view vaccinations for this pet")
        
        return self.vaccination_repository.get_upcoming_vaccinations(pet_id, days=days)
    
    def update_vaccination(
        self,
        vaccination_id: str,
        vaccination_data: VaccinationUpdate,
        current_user: User
    ) -> Optional[Vaccination]:
        """Update a vaccination record (limited fields)."""
        existing = self.vaccination_repository.get_by_id(vaccination_id)
        
        if not existing:
            return None
        
        # Only doctors can update vaccinations
        if not self.permission_service.can_create_vaccinations(
            current_user,
            str(existing.pet_id)
        ):
            raise PermissionError("Only doctors can update vaccinations")
        
        # Prepare update data
        update_data = {}
        if vaccination_data.next_due_date is not None:
            update_data["next_due_date"] = vaccination_data.next_due_date
        if vaccination_data.reaction_notes is not None:
            update_data["reaction_notes"] = vaccination_data.reaction_notes
        if vaccination_data.certificate_url is not None:
            update_data["certificate_url"] = vaccination_data.certificate_url
        
        return self.vaccination_repository.update(vaccination_id, **update_data)
    
    def get_required_by_law_vaccinations(
        self,
        pet_id: str,
        current_user: User
    ) -> List[Vaccination]:
        """Get legally required vaccinations for a pet."""
        if not self.permission_service.can_read_vaccinations(current_user, pet_id):
            raise PermissionError("You don't have permission to view vaccinations for this pet")
        
        return self.vaccination_repository.get_required_by_law(pet_id)

