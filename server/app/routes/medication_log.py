"""
Medication Log routes for API endpoints.

This module defines all medication log-related API endpoints with proper
dependency injection and request/response handling.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.controllers.medication_log_controller import MedicationLogController
from app.database import get_db_session
from app.dependencies import get_current_user_id
from app.schemas.medication_log import (
    MedicationLogCreate,
    MedicationLogUpdate,
    MedicationLogResponse,
    MedicationLogListResponse
)


# Create router
router = APIRouter(prefix="/pets", tags=["medication-logs"])


# Dependency to get medication log controller
def get_medication_log_controller(
    db: Session = Depends(get_db_session)
) -> MedicationLogController:
    """Get medication log controller with dependency injection."""
    from app.repositories.medication_log_repository import MedicationLogRepository
    from app.repositories.pet import PetRepository
    from app.services.medication_log_service import MedicationLogService
    
    med_log_repo = MedicationLogRepository(db)
    pet_repo = PetRepository(db)
    med_log_service = MedicationLogService(med_log_repo, pet_repo)
    return MedicationLogController(med_log_service)


# API Endpoints
@router.post(
    "/{pet_id}/medications",
    response_model=MedicationLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log medication administration",
    description="Log when a medication was given to a pet"
)
def log_medication(
    pet_id: str,
    log_data: MedicationLogCreate,
    user_id: int = Depends(get_current_user_id),
    controller: MedicationLogController = Depends(get_medication_log_controller)
) -> MedicationLogResponse:
    """
    Log medication administration for a pet.
    
    This endpoint allows pet owners to track when they give medication to their pets,
    including the dosage, time, and any notes.
    """
    # Set pet_id from URL path
    log_data.pet_id = pet_id
    return controller.log_medication(log_data, user_id)


@router.get(
    "/{pet_id}/medications",
    response_model=MedicationLogListResponse,
    summary="Get medication logs",
    description="Retrieve all medication logs for a pet"
)
def get_medication_logs(
    pet_id: str,
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    user_id: int = Depends(get_current_user_id),
    controller: MedicationLogController = Depends(get_medication_log_controller)
) -> MedicationLogListResponse:
    """Get all medication logs for a pet with pagination."""
    return controller.get_medication_logs_by_pet(pet_id, skip, limit)


@router.get(
    "/{pet_id}/medications/recent",
    response_model=MedicationLogListResponse,
    summary="Get recent medication logs",
    description="Retrieve recent medication logs for a pet"
)
def get_recent_medication_logs(
    pet_id: str,
    days: int = Query(default=7, ge=1, le=90, description="Number of days to look back"),
    user_id: int = Depends(get_current_user_id),
    controller: MedicationLogController = Depends(get_medication_log_controller)
) -> MedicationLogListResponse:
    """Get recent medication logs for a pet (default: last 7 days)."""
    return controller.get_recent_medication_logs(pet_id, days)


@router.get(
    "/{pet_id}/medications/date-range",
    response_model=MedicationLogListResponse,
    summary="Get medication logs by date range",
    description="Retrieve medication logs within a specific date range"
)
def get_medication_logs_by_date_range(
    pet_id: str,
    start_date: datetime = Query(..., description="Start datetime (inclusive)"),
    end_date: datetime = Query(..., description="End datetime (inclusive)"),
    user_id: int = Depends(get_current_user_id),
    controller: MedicationLogController = Depends(get_medication_log_controller)
) -> MedicationLogListResponse:
    """Get medication logs within a date range."""
    return controller.get_medication_logs_by_date_range(pet_id, start_date, end_date)


@router.get(
    "/{pet_id}/medications/history/{medication_name}",
    summary="Get medication history",
    description="Get complete history for a specific medication"
)
def get_medication_history(
    pet_id: str,
    medication_name: str,
    user_id: int = Depends(get_current_user_id),
    controller: MedicationLogController = Depends(get_medication_log_controller)
) -> dict:
    """Get complete medication history for a specific medication."""
    return controller.get_medication_history(pet_id, medication_name)


@router.get(
    "/{pet_id}/medications/{log_id}",
    response_model=MedicationLogResponse,
    summary="Get a specific medication log",
    description="Retrieve a specific medication log by ID"
)
def get_medication_log(
    pet_id: str,
    log_id: str,
    user_id: int = Depends(get_current_user_id),
    controller: MedicationLogController = Depends(get_medication_log_controller)
) -> MedicationLogResponse:
    """Get a specific medication log by ID."""
    return controller.get_medication_log(log_id)


@router.put(
    "/{pet_id}/medications/{log_id}",
    response_model=MedicationLogResponse,
    summary="Update a medication log",
    description="Update an existing medication log"
)
def update_medication_log(
    pet_id: str,
    log_id: str,
    update_data: MedicationLogUpdate,
    user_id: int = Depends(get_current_user_id),
    controller: MedicationLogController = Depends(get_medication_log_controller)
) -> MedicationLogResponse:
    """Update an existing medication log."""
    return controller.update_medication_log(log_id, update_data, user_id)


@router.delete(
    "/{pet_id}/medications/{log_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a medication log",
    description="Delete an existing medication log"
)
def delete_medication_log(
    pet_id: str,
    log_id: str,
    user_id: int = Depends(get_current_user_id),
    controller: MedicationLogController = Depends(get_medication_log_controller)
) -> dict:
    """Delete a medication log."""
    return controller.delete_medication_log(log_id, user_id)


# Health check endpoint
@router.get(
    "/medications/health",
    summary="Medication Log service health check",
    description="Check if medication log service is running"
)
async def health_check() -> dict:
    """Health check endpoint."""
    return {"message": "Medication Log service is running"}

