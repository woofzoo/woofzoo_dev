"""
Medication Log service for business logic operations.

This module provides the MedicationLogService class for owner-managed medication
log operations, acting as an intermediary between controllers and repositories.
"""

from datetime import datetime, timedelta
from typing import List, Optional
import uuid

from app.models.medication_log import MedicationLog
from app.repositories.medication_log_repository import MedicationLogRepository
from app.repositories.pet import PetRepository
from app.schemas.medication_log import MedicationLogCreate, MedicationLogUpdate
from loguru import logger


class MedicationLogService:
    """
    Medication Log service for business logic operations.
    
    This class handles business logic for owner-managed medication log operations,
    including validation, permissions, and coordination between repositories.
    """
    
    def __init__(
        self, 
        medication_log_repository: MedicationLogRepository,
        pet_repository: PetRepository
    ) -> None:
        """
        Initialize the medication log service.
        
        Args:
            medication_log_repository: Repository for medication log operations
            pet_repository: Repository for pet operations
        """
        self.medication_log_repository = medication_log_repository
        self.pet_repository = pet_repository
    
    def log_medication(
        self, 
        log_data: MedicationLogCreate,
        user_id: int
    ) -> MedicationLog:
        """
        Log a medication administration for a pet.
        
        Args:
            log_data: Medication log data
            user_id: ID of the user logging the medication
            
        Returns:
            Created medication log
            
        Raises:
            ValueError: If pet not found or validation fails
        """
        # Convert pet_id string to UUID
        try:
            pet_id_uuid = uuid.UUID(log_data.pet_id)
        except (ValueError, AttributeError):
            raise ValueError(f"Invalid pet_id format: {log_data.pet_id}")
        
        # Verify pet exists
        pet = self.pet_repository.get_by_id(pet_id_uuid)
        if not pet:
            raise ValueError(f"Pet with ID {log_data.pet_id} not found")
        
        # Create the medication log
        log = self.medication_log_repository.create(
            pet_id=pet_id_uuid,
            created_by_user_id=user_id,
            medication_name=log_data.medication_name,
            dosage=log_data.dosage,
            dosage_unit=log_data.dosage_unit,
            administered_at=log_data.administered_at,
            notes=log_data.notes
        )
        
        logger.info(
            "Medication logged",
            extra={
                "log_id": str(log.id),
                "pet_id": str(pet_id_uuid),
                "medication_name": log_data.medication_name,
                "user_id": user_id
            }
        )
        
        return log
    
    def get_medication_log_by_id(self, log_id: uuid.UUID) -> Optional[MedicationLog]:
        """
        Get a medication log by ID.
        
        Args:
            log_id: Medication log unique identifier
            
        Returns:
            Medication log or None if not found
        """
        return self.medication_log_repository.get_by_id(log_id)
    
    def get_medication_logs_by_pet(
        self,
        pet_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[MedicationLog]:
        """
        Get medication logs for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of medication logs
        """
        return self.medication_log_repository.get_by_pet_id(pet_id, skip, limit)
    
    def get_recent_medication_logs(
        self,
        pet_id: uuid.UUID,
        days: int = 7
    ) -> List[MedicationLog]:
        """
        Get recent medication logs for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            days: Number of days to look back (default: 7)
            
        Returns:
            List of recent medication logs
        """
        return self.medication_log_repository.get_recent_medications(pet_id, days)
    
    def get_medication_logs_by_date_range(
        self,
        pet_id: uuid.UUID,
        start_date: datetime,
        end_date: datetime
    ) -> List[MedicationLog]:
        """
        Get medication logs within a date range.
        
        Args:
            pet_id: Pet's unique identifier
            start_date: Start datetime of range (inclusive)
            end_date: End datetime of range (inclusive)
            
        Returns:
            List of medication logs
        """
        return self.medication_log_repository.get_by_date_range(
            pet_id, start_date, end_date
        )
    
    def get_medication_logs_by_name(
        self,
        pet_id: uuid.UUID,
        medication_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[MedicationLog]:
        """
        Get medication logs by medication name.
        
        Args:
            pet_id: Pet's unique identifier
            medication_name: Name of the medication
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of medication logs
        """
        return self.medication_log_repository.get_by_medication_name(
            pet_id, medication_name, skip, limit
        )
    
    def update_medication_log(
        self,
        log_id: uuid.UUID,
        update_data: MedicationLogUpdate,
        user_id: int
    ) -> Optional[MedicationLog]:
        """
        Update a medication log.
        
        Args:
            log_id: Medication log unique identifier
            update_data: Update data
            user_id: ID of the user updating the log
            
        Returns:
            Updated medication log or None if not found
            
        Raises:
            ValueError: If user doesn't have permission to update
        """
        log = self.medication_log_repository.get_by_id(log_id)
        if not log:
            return None
        
        # Only allow the creator to update (can be extended for family members)
        if log.created_by_user_id != user_id:
            raise ValueError("You don't have permission to update this medication log")
        
        # Prepare update data
        update_dict = update_data.model_dump(exclude_unset=True)
        
        updated_log = self.medication_log_repository.update(log_id, **update_dict)
        
        logger.info(
            "Medication log updated",
            extra={
                "log_id": str(log_id),
                "user_id": user_id
            }
        )
        
        return updated_log
    
    def delete_medication_log(self, log_id: uuid.UUID, user_id: int) -> bool:
        """
        Delete a medication log.
        
        Args:
            log_id: Medication log unique identifier
            user_id: ID of the user deleting the log
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If user doesn't have permission to delete
        """
        log = self.medication_log_repository.get_by_id(log_id)
        if not log:
            return False
        
        # Only allow the creator to delete (can be extended for family members)
        if log.created_by_user_id != user_id:
            raise ValueError("You don't have permission to delete this medication log")
        
        result = self.medication_log_repository.delete(log_id)
        
        if result:
            logger.info(
                "Medication log deleted",
                extra={
                    "log_id": str(log_id),
                    "user_id": user_id
                }
            )
        
        return result
    
    def count_medication_logs(self, pet_id: uuid.UUID) -> int:
        """
        Count total medication logs for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            
        Returns:
            Total count of medication logs
        """
        return self.medication_log_repository.count_by_pet_id(pet_id)
    
    def get_medication_history(
        self,
        pet_id: uuid.UUID,
        medication_name: str
    ) -> dict:
        """
        Get medication history for a specific medication.
        
        Args:
            pet_id: Pet's unique identifier
            medication_name: Name of the medication
            
        Returns:
            Dictionary with medication history summary
        """
        logs = self.medication_log_repository.get_by_medication_name(
            pet_id, medication_name
        )
        
        if not logs:
            return {
                "medication_name": medication_name,
                "total_administrations": 0,
                "last_administered": None,
                "logs": []
            }
        
        return {
            "medication_name": medication_name,
            "total_administrations": len(logs),
            "last_administered": logs[0].administered_at.isoformat() if logs else None,
            "logs": [log.to_dict() for log in logs]
        }

