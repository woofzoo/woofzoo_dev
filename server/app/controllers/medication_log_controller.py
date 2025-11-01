"""
Medication Log controller for API layer.

This module provides the MedicationLogController class for handling HTTP requests
and responses related to medication log operations.
"""

from datetime import datetime
from typing import Optional
import uuid

from fastapi import HTTPException, status

from app.schemas.medication_log import (
    MedicationLogCreate,
    MedicationLogUpdate,
    MedicationLogResponse,
    MedicationLogListResponse
)
from app.services.medication_log_service import MedicationLogService
from loguru import logger


class MedicationLogController:
    """
    Medication Log controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to medication log operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, medication_log_service: MedicationLogService) -> None:
        """
        Initialize the medication log controller.
        
        Args:
            medication_log_service: Service for medication log operations
        """
        self.medication_log_service = medication_log_service
    
    def log_medication(
        self,
        log_data: MedicationLogCreate,
        user_id: int
    ) -> MedicationLogResponse:
        """
        Log a medication administration for a pet.
        
        Args:
            log_data: Medication log data
            user_id: ID of the authenticated user
            
        Returns:
            Created medication log response
            
        Raises:
            HTTPException: If logging fails
        """
        try:
            logger.info(
                "Logging medication",
                extra={
                    "pet_id": log_data.pet_id,
                    "medication_name": log_data.medication_name,
                    "user_id": user_id
                }
            )
            log = self.medication_log_service.log_medication(log_data, user_id)
            logger.info(
                "Medication logged successfully",
                extra={"log_id": str(log.id)}
            )
            return MedicationLogResponse.model_validate(log)
        except ValueError as e:
            logger.warning("Medication logging failed", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error logging medication")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to log medication"
            )
    
    def get_medication_log(self, log_id: str) -> MedicationLogResponse:
        """
        Get a specific medication log.
        
        Args:
            log_id: Medication log unique identifier
            
        Returns:
            Medication log response
            
        Raises:
            HTTPException: If log not found
        """
        try:
            log_uuid = uuid.UUID(log_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid log_id format: {log_id}"
            )
        
        log = self.medication_log_service.get_medication_log_by_id(log_uuid)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Medication log with ID {log_id} not found"
            )
        
        return MedicationLogResponse.model_validate(log)
    
    def get_medication_logs_by_pet(
        self,
        pet_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> MedicationLogListResponse:
        """
        Get medication logs for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of medication logs
            
        Raises:
            HTTPException: If pet ID is invalid
        """
        try:
            pet_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid pet_id format: {pet_id}"
            )
        
        try:
            logs = self.medication_log_service.get_medication_logs_by_pet(
                pet_uuid, skip, limit
            )
            total = self.medication_log_service.count_medication_logs(pet_uuid)
            
            return MedicationLogListResponse(
                logs=[MedicationLogResponse.model_validate(log) for log in logs],
                total=total
            )
        except Exception as e:
            logger.exception("Error retrieving medication logs")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve medication logs"
            )
    
    def get_recent_medication_logs(
        self,
        pet_id: str,
        days: int = 7
    ) -> MedicationLogListResponse:
        """
        Get recent medication logs for a pet.
        
        Args:
            pet_id: Pet's unique identifier
            days: Number of days to look back
            
        Returns:
            List of recent medication logs
            
        Raises:
            HTTPException: If pet ID is invalid
        """
        try:
            pet_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid pet_id format: {pet_id}"
            )
        
        try:
            logs = self.medication_log_service.get_recent_medication_logs(
                pet_uuid, days
            )
            
            return MedicationLogListResponse(
                logs=[MedicationLogResponse.model_validate(log) for log in logs],
                total=len(logs)
            )
        except Exception as e:
            logger.exception("Error retrieving recent medication logs")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve recent medication logs"
            )
    
    def get_medication_logs_by_date_range(
        self,
        pet_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> MedicationLogListResponse:
        """
        Get medication logs within a date range.
        
        Args:
            pet_id: Pet's unique identifier
            start_date: Start datetime of range
            end_date: End datetime of range
            
        Returns:
            List of medication logs
            
        Raises:
            HTTPException: If pet ID is invalid
        """
        try:
            pet_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid pet_id format: {pet_id}"
            )
        
        try:
            logs = self.medication_log_service.get_medication_logs_by_date_range(
                pet_uuid, start_date, end_date
            )
            
            return MedicationLogListResponse(
                logs=[MedicationLogResponse.model_validate(log) for log in logs],
                total=len(logs)
            )
        except Exception as e:
            logger.exception("Error retrieving medication logs by date range")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve medication logs"
            )
    
    def update_medication_log(
        self,
        log_id: str,
        update_data: MedicationLogUpdate,
        user_id: int
    ) -> MedicationLogResponse:
        """
        Update a medication log.
        
        Args:
            log_id: Medication log unique identifier
            update_data: Update data
            user_id: ID of the authenticated user
            
        Returns:
            Updated medication log response
            
        Raises:
            HTTPException: If update fails
        """
        try:
            log_uuid = uuid.UUID(log_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid log_id format: {log_id}"
            )
        
        try:
            updated_log = self.medication_log_service.update_medication_log(
                log_uuid, update_data, user_id
            )
            if not updated_log:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Medication log with ID {log_id} not found"
                )
            
            logger.info("Medication log updated", extra={"log_id": log_id})
            return MedicationLogResponse.model_validate(updated_log)
        except ValueError as e:
            logger.warning("Medication log update failed", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error updating medication log")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update medication log"
            )
    
    def delete_medication_log(self, log_id: str, user_id: int) -> dict:
        """
        Delete a medication log.
        
        Args:
            log_id: Medication log unique identifier
            user_id: ID of the authenticated user
            
        Returns:
            Success message
            
        Raises:
            HTTPException: If deletion fails
        """
        try:
            log_uuid = uuid.UUID(log_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid log_id format: {log_id}"
            )
        
        try:
            success = self.medication_log_service.delete_medication_log(log_uuid, user_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Medication log with ID {log_id} not found"
                )
            
            logger.info("Medication log deleted", extra={"log_id": log_id})
            return {"message": "Medication log deleted successfully"}
        except ValueError as e:
            logger.warning("Medication log deletion failed", extra={"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception("Unexpected error deleting medication log")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete medication log"
            )
    
    def get_medication_history(
        self,
        pet_id: str,
        medication_name: str
    ) -> dict:
        """
        Get medication history for a specific medication.
        
        Args:
            pet_id: Pet's unique identifier
            medication_name: Name of the medication
            
        Returns:
            Medication history summary
            
        Raises:
            HTTPException: If pet ID is invalid
        """
        try:
            pet_uuid = uuid.UUID(pet_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid pet_id format: {pet_id}"
            )
        
        try:
            history = self.medication_log_service.get_medication_history(
                pet_uuid, medication_name
            )
            return history
        except Exception as e:
            logger.exception("Error retrieving medication history")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve medication history"
            )

