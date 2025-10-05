"""
Medical Record Service for business logic operations.

This module provides the MedicalRecordService class for medical record-related
business logic with access control.
"""

from typing import List, Optional
from datetime import datetime
import uuid

from app.models.medical_record import MedicalRecord
from app.models.user import User
from app.repositories.medical_record import MedicalRecordRepository
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate
from app.services.permission_service import PermissionService


class MedicalRecordService:
    """
    Medical Record service for business logic operations.
    
    This class handles business logic for medical record operations,
    including validation, access control, and coordination.
    """
    
    def __init__(
        self,
        medical_record_repository: MedicalRecordRepository,
        permission_service: PermissionService
    ):
        """Initialize the medical record service."""
        self.medical_record_repository = medical_record_repository
        self.permission_service = permission_service
    
    def create_medical_record(
        self,
        record_data: MedicalRecordCreate,
        current_user: User
    ) -> Optional[MedicalRecord]:
        """
        Create a new medical record with access control.
        
        Args:
            record_data: Medical record data
            current_user: User creating the record
            
        Returns:
            Created MedicalRecord or None if unauthorized
            
        Raises:
            PermissionError: If user doesn't have permission
        """
        # Check if user can create medical records for this pet
        can_create, user_role = self.permission_service.can_create_medical_records(
            current_user,
            record_data.pet_id
        )
        
        if not can_create:
            raise PermissionError("You don't have permission to create medical records for this pet")
        
        # Convert UUID strings
        try:
            pet_id_uuid = uuid.UUID(record_data.pet_id)
            clinic_id_uuid = uuid.UUID(record_data.clinic_id)
            doctor_id_uuid = uuid.UUID(record_data.doctor_id)
        except ValueError as e:
            raise ValueError(f"Invalid UUID format: {e}")
        
        # Create the medical record
        record = self.medical_record_repository.create(
            pet_id=pet_id_uuid,
            visit_date=record_data.visit_date,
            clinic_id=clinic_id_uuid,
            doctor_id=doctor_id_uuid,
            visit_type=record_data.visit_type,
            chief_complaint=record_data.chief_complaint,
            diagnosis=record_data.diagnosis,
            symptoms=record_data.symptoms or {},
            treatment_plan=record_data.treatment_plan,
            clinical_notes=record_data.clinical_notes,
            weight=record_data.weight,
            temperature=record_data.temperature,
            vital_signs=record_data.vital_signs or {},
            follow_up_required=record_data.follow_up_required,
            follow_up_date=record_data.follow_up_date,
            follow_up_notes=record_data.follow_up_notes,
            is_emergency=record_data.is_emergency,
            created_by_user_id=current_user.public_id,
            created_by_role=user_role
        )
        
        return record
    
    def get_medical_record(
        self,
        record_id: str,
        current_user: User
    ) -> Optional[MedicalRecord]:
        """
        Get a medical record by ID with access control.
        
        Args:
            record_id: Medical record ID
            current_user: User requesting the record
            
        Returns:
            MedicalRecord or None if not found/unauthorized
        """
        record = self.medical_record_repository.get_by_id(record_id)
        
        if not record:
            return None
        
        # Check if user can read this pet's medical records
        if not self.permission_service.can_read_pet_medical_records(
            current_user,
            str(record.pet_id)
        ):
            raise PermissionError("You don't have permission to view this medical record")
        
        return record
    
    def get_medical_records_by_pet(
        self,
        pet_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[MedicalRecord]:
        """
        Get all medical records for a pet with access control.
        
        Args:
            pet_id: Pet's ID
            current_user: User requesting the records
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecord instances
        """
        # Check if user can read this pet's medical records
        if not self.permission_service.can_read_pet_medical_records(current_user, pet_id):
            raise PermissionError("You don't have permission to view medical records for this pet")
        
        return self.medical_record_repository.get_by_pet_id(pet_id, skip=skip, limit=limit)
    
    def get_medical_records_by_date_range(
        self,
        pet_id: str,
        start_date: datetime,
        end_date: datetime,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[MedicalRecord]:
        """
        Get medical records for a pet within a date range.
        
        Args:
            pet_id: Pet's ID
            start_date: Start date
            end_date: End date
            current_user: User requesting the records
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecord instances
        """
        # Check if user can read this pet's medical records
        if not self.permission_service.can_read_pet_medical_records(current_user, pet_id):
            raise PermissionError("You don't have permission to view medical records for this pet")
        
        return self.medical_record_repository.get_by_pet_id_date_range(
            pet_id,
            start_date,
            end_date,
            skip=skip,
            limit=limit
        )
    
    def update_medical_record(
        self,
        record_id: str,
        record_data: MedicalRecordUpdate,
        current_user: User
    ) -> Optional[MedicalRecord]:
        """
        Update a medical record (admin corrections only).
        
        Args:
            record_id: Medical record ID
            record_data: Update data
            current_user: User updating the record
            
        Returns:
            Updated MedicalRecord or None if not found
        """
        # Get existing record
        existing_record = self.medical_record_repository.get_by_id(record_id)
        
        if not existing_record:
            return None
        
        # Check if user can update this record
        if not self.permission_service.can_update_medical_records(
            current_user,
            str(existing_record.pet_id),
            existing_record.created_by_role
        ):
            raise PermissionError("You don't have permission to update this medical record")
        
        # Prepare update data (only allowed fields)
        update_data = {}
        if record_data.diagnosis is not None:
            update_data["diagnosis"] = record_data.diagnosis
        if record_data.treatment_plan is not None:
            update_data["treatment_plan"] = record_data.treatment_plan
        if record_data.clinical_notes is not None:
            update_data["clinical_notes"] = record_data.clinical_notes
        if record_data.follow_up_required is not None:
            update_data["follow_up_required"] = record_data.follow_up_required
        if record_data.follow_up_date is not None:
            update_data["follow_up_date"] = record_data.follow_up_date
        if record_data.follow_up_notes is not None:
            update_data["follow_up_notes"] = record_data.follow_up_notes
        
        # Update the record
        return self.medical_record_repository.update(record_id, **update_data)
    
    def get_emergency_records(
        self,
        pet_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> List[MedicalRecord]:
        """Get emergency medical records for a pet."""
        if not self.permission_service.can_read_pet_medical_records(current_user, pet_id):
            raise PermissionError("You don't have permission to view medical records for this pet")
        
        return self.medical_record_repository.get_emergency_records(pet_id, skip=skip, limit=limit)
    
    def get_records_requiring_followup(
        self,
        pet_id: str,
        current_user: User
    ) -> List[MedicalRecord]:
        """Get medical records requiring follow-up for a pet."""
        if not self.permission_service.can_read_pet_medical_records(current_user, pet_id):
            raise PermissionError("You don't have permission to view medical records for this pet")
        
        return self.medical_record_repository.get_records_requiring_followup(pet_id)

