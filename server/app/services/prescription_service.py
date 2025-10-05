"""
Prescription Service for business logic operations.

This module provides the PrescriptionService class for prescription-related
business logic with access control.
"""

from typing import List, Optional
import uuid

from app.models.prescription import Prescription
from app.models.user import User
from app.repositories.prescription import PrescriptionRepository
from app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate
from app.services.permission_service import PermissionService


class PrescriptionService:
    """
    Prescription service for business logic operations.
    
    This class handles business logic for prescription operations,
    including validation, access control, and coordination.
    """
    
    def __init__(
        self,
        prescription_repository: PrescriptionRepository,
        permission_service: PermissionService
    ):
        """Initialize the prescription service."""
        self.prescription_repository = prescription_repository
        self.permission_service = permission_service
    
    def create_prescription(
        self,
        prescription_data: PrescriptionCreate,
        current_user: User
    ) -> Optional[Prescription]:
        """
        Create a new prescription with access control.
        
        Args:
            prescription_data: Prescription data
            current_user: User creating the prescription
            
        Returns:
            Created Prescription or None if unauthorized
        """
        # Only doctors can create prescriptions
        if not self.permission_service.can_create_prescriptions(
            current_user,
            prescription_data.pet_id
        ):
            raise PermissionError("Only doctors can create prescriptions")
        
        # Convert UUID strings
        try:
            medical_record_id_uuid = uuid.UUID(prescription_data.medical_record_id)
            pet_id_uuid = uuid.UUID(prescription_data.pet_id)
            doctor_id_uuid = uuid.UUID(prescription_data.prescribed_by_doctor_id)
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {e}")
        
        # Create the prescription
        prescription = self.prescription_repository.create(
            medical_record_id=medical_record_id_uuid,
            pet_id=pet_id_uuid,
            medication_name=prescription_data.medication_name,
            dosage=prescription_data.dosage,
            dosage_unit=prescription_data.dosage_unit,
            frequency=prescription_data.frequency,
            route=prescription_data.route,
            duration=prescription_data.duration,
            instructions=prescription_data.instructions,
            prescribed_by_doctor_id=doctor_id_uuid,
            prescribed_date=prescription_data.prescribed_date,
            start_date=prescription_data.start_date,
            end_date=prescription_data.end_date,
            quantity=prescription_data.quantity,
            refills_allowed=prescription_data.refills_allowed,
            is_active=True
        )
        
        return prescription
    
    def get_prescription(
        self,
        prescription_id: str,
        current_user: User
    ) -> Optional[Prescription]:
        """Get a prescription by ID with access control."""
        prescription = self.prescription_repository.get_by_id(prescription_id)
        
        if not prescription:
            return None
        
        if not self.permission_service.can_read_prescriptions(
            current_user,
            str(prescription.pet_id)
        ):
            raise PermissionError("You don't have permission to view this prescription")
        
        return prescription
    
    def get_prescriptions_by_pet(
        self,
        pet_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[Prescription]:
        """Get all prescriptions for a pet with access control."""
        if not self.permission_service.can_read_prescriptions(current_user, pet_id):
            raise PermissionError("You don't have permission to view prescriptions for this pet")
        
        return self.prescription_repository.get_by_pet_id(pet_id, skip=skip, limit=limit)
    
    def get_active_prescriptions(
        self,
        pet_id: str,
        current_user: User
    ) -> List[Prescription]:
        """Get active prescriptions for a pet."""
        if not self.permission_service.can_read_prescriptions(current_user, pet_id):
            raise PermissionError("You don't have permission to view prescriptions for this pet")
        
        return self.prescription_repository.get_active_prescriptions(pet_id)
    
    def update_prescription(
        self,
        prescription_id: str,
        prescription_data: PrescriptionUpdate,
        current_user: User
    ) -> Optional[Prescription]:
        """Update a prescription (limited fields)."""
        existing = self.prescription_repository.get_by_id(prescription_id)
        
        if not existing:
            return None
        
        # Only doctors can update prescriptions
        if not self.permission_service.can_create_prescriptions(
            current_user,
            str(existing.pet_id)
        ):
            raise PermissionError("Only doctors can update prescriptions")
        
        # Prepare update data
        update_data = {}
        if prescription_data.end_date is not None:
            update_data["end_date"] = prescription_data.end_date
        if prescription_data.is_active is not None:
            update_data["is_active"] = prescription_data.is_active
        if prescription_data.instructions is not None:
            update_data["instructions"] = prescription_data.instructions
        
        return self.prescription_repository.update(prescription_id, **update_data)
    
    def get_expiring_prescriptions(
        self,
        pet_id: str,
        current_user: User,
        days: int = 7
    ) -> List[Prescription]:
        """Get prescriptions expiring soon."""
        if not self.permission_service.can_read_prescriptions(current_user, pet_id):
            raise PermissionError("You don't have permission to view prescriptions for this pet")
        
        return self.prescription_repository.get_expiring_soon(pet_id, days=days)

