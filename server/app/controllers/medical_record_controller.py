"""
Medical Record controller for API layer.

This module provides the MedicalRecordController class for handling HTTP requests
and responses related to medical record operations.
"""

from typing import List
from datetime import datetime

from fastapi import HTTPException, status
from loguru import logger

from app.models.user import User
from app.schemas.medical_record import (
    MedicalRecordCreate, 
    MedicalRecordResponse, 
    MedicalRecordUpdate,
    MedicalRecordListResponse
)
from app.services.medical_record_service import MedicalRecordService


class MedicalRecordController:
    """
    Medical Record controller for handling HTTP requests and responses.
    
    This class handles HTTP requests related to medical record operations,
    including request validation, response formatting, and error handling.
    """
    
    def __init__(self, medical_record_service: MedicalRecordService):
        """Initialize the medical record controller."""
        self.medical_record_service = medical_record_service
    
    def create_medical_record(
        self,
        record_data: MedicalRecordCreate,
        current_user: User
    ) -> MedicalRecordResponse:
        """Create a new medical record."""
        try:
            logger.info(
                "Creating medical record",
                extra={
                    "pet_id": record_data.pet_id,
                    "visit_type": record_data.visit_type,
                    "user_id": str(current_user.id)
                }
            )
            
            record = self.medical_record_service.create_medical_record(
                record_data,
                current_user
            )
            
            logger.info(
                "Medical record created successfully",
                extra={"record_id": str(record.id), "pet_id": str(record.pet_id)}
            )
            
            return MedicalRecordResponse.model_validate(record)
            
        except PermissionError as e:
            logger.warning(
                "Medical record creation denied - permission error",
                extra={"error": str(e), "user_id": str(current_user.id)}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except ValueError as e:
            logger.warning(
                "Medical record creation failed - validation error",
                extra={"error": str(e)}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Medical record creation failed - unexpected error",
                extra={"pet_id": record_data.pet_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create medical record"
            )
    
    def get_medical_record(
        self,
        record_id: str,
        current_user: User
    ) -> MedicalRecordResponse:
        """Get a medical record by ID."""
        try:
            record = self.medical_record_service.get_medical_record(
                record_id,
                current_user
            )
            
            if not record:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Medical record with ID {record_id} not found"
                )
            
            return MedicalRecordResponse.model_validate(record)
            
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Failed to get medical record",
                extra={"record_id": record_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve medical record"
            )
    
    def get_medical_records_by_pet(
        self,
        pet_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> MedicalRecordListResponse:
        """Get all medical records for a pet."""
        try:
            records = self.medical_record_service.get_medical_records_by_pet(
                pet_id,
                current_user,
                skip=skip,
                limit=limit
            )
            
            record_responses = [
                MedicalRecordResponse.model_validate(record) 
                for record in records
            ]
            
            return MedicalRecordListResponse(
                records=record_responses,
                total=len(records),
                skip=skip,
                limit=limit
            )
            
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Failed to get medical records",
                extra={"pet_id": pet_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve medical records"
            )
    
    def get_medical_records_by_date_range(
        self,
        pet_id: str,
        start_date: datetime,
        end_date: datetime,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> MedicalRecordListResponse:
        """Get medical records for a pet within a date range."""
        try:
            records = self.medical_record_service.get_medical_records_by_date_range(
                pet_id,
                start_date,
                end_date,
                current_user,
                skip=skip,
                limit=limit
            )
            
            record_responses = [
                MedicalRecordResponse.model_validate(record) 
                for record in records
            ]
            
            return MedicalRecordListResponse(
                records=record_responses,
                total=len(records),
                skip=skip,
                limit=limit
            )
            
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Failed to get medical records by date range",
                extra={"pet_id": pet_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve medical records"
            )
    
    def update_medical_record(
        self,
        record_id: str,
        record_data: MedicalRecordUpdate,
        current_user: User
    ) -> MedicalRecordResponse:
        """Update a medical record (admin corrections only)."""
        try:
            record = self.medical_record_service.update_medical_record(
                record_id,
                record_data,
                current_user
            )
            
            if not record:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Medical record with ID {record_id} not found"
                )
            
            logger.info(
                "Medical record updated",
                extra={"record_id": record_id, "user_id": str(current_user.id)}
            )
            
            return MedicalRecordResponse.model_validate(record)
            
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Failed to update medical record",
                extra={"record_id": record_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update medical record"
            )
    
    def get_emergency_records(
        self,
        pet_id: str,
        current_user: User,
        skip: int = 0,
        limit: int = 100
    ) -> MedicalRecordListResponse:
        """Get emergency medical records for a pet."""
        try:
            records = self.medical_record_service.get_emergency_records(
                pet_id,
                current_user,
                skip=skip,
                limit=limit
            )
            
            record_responses = [
                MedicalRecordResponse.model_validate(record) 
                for record in records
            ]
            
            return MedicalRecordListResponse(
                records=record_responses,
                total=len(records),
                skip=skip,
                limit=limit
            )
            
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            logger.exception(
                "Failed to get emergency records",
                extra={"pet_id": pet_id}
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve emergency records"
            )

