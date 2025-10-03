"""
Medical Record routes for API endpoints.
"""

from fastapi import APIRouter, Depends, Query, status
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from app.controllers.medical_record_controller import MedicalRecordController
from app.services.medical_record_service import MedicalRecordService
from app.services.permission_service import PermissionService
from app.repositories.medical_record import MedicalRecordRepository
from app.repositories.pet import PetRepository
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from app.dependencies import get_current_user, get_db_session
from app.models.user import User
from app.schemas.medical_record import (
    MedicalRecordCreate, 
    MedicalRecordResponse, 
    MedicalRecordUpdate,
    MedicalRecordListResponse
)

router = APIRouter(prefix="/medical-records", tags=["medical-records"])


def get_medical_record_controller(db: Session = Depends(get_db_session)) -> MedicalRecordController:
    """Dependency injection for medical record controller."""
    medical_record_repo = MedicalRecordRepository(db)
    pet_repo = PetRepository(db)
    clinic_access_repo = PetClinicAccessRepository(db)
    permission_service = PermissionService(pet_repo, clinic_access_repo)
    service = MedicalRecordService(medical_record_repo, permission_service)
    return MedicalRecordController(service)


@router.post("/", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
def create_medical_record(
    record_data: MedicalRecordCreate,
    current_user: User = Depends(get_current_user),
    controller: MedicalRecordController = Depends(get_medical_record_controller)
):
    """Create a new medical record."""
    return controller.create_medical_record(record_data, current_user)


@router.get("/{record_id}", response_model=MedicalRecordResponse)
def get_medical_record(
    record_id: str,
    current_user: User = Depends(get_current_user),
    controller: MedicalRecordController = Depends(get_medical_record_controller)
):
    """Get a medical record by ID."""
    return controller.get_medical_record(record_id, current_user)


@router.get("/pet/{pet_id}", response_model=MedicalRecordListResponse)
def get_medical_records_by_pet(
    pet_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    controller: MedicalRecordController = Depends(get_medical_record_controller)
):
    """Get all medical records for a pet."""
    return controller.get_medical_records_by_pet(pet_id, current_user, skip, limit)


@router.get("/pet/{pet_id}/date-range", response_model=MedicalRecordListResponse)
def get_medical_records_by_date_range(
    pet_id: str,
    start_date: datetime,
    end_date: datetime,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    controller: MedicalRecordController = Depends(get_medical_record_controller)
):
    """Get medical records for a pet within a date range."""
    return controller.get_medical_records_by_date_range(pet_id, start_date, end_date, current_user, skip, limit)


@router.get("/pet/{pet_id}/emergency", response_model=MedicalRecordListResponse)
def get_emergency_records(
    pet_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    controller: MedicalRecordController = Depends(get_medical_record_controller)
):
    """Get emergency medical records for a pet."""
    return controller.get_emergency_records(pet_id, current_user, skip, limit)


@router.put("/{record_id}", response_model=MedicalRecordResponse)
def update_medical_record(
    record_id: str,
    record_data: MedicalRecordUpdate,
    current_user: User = Depends(get_current_user),
    controller: MedicalRecordController = Depends(get_medical_record_controller)
):
    """Update a medical record (admin corrections only)."""
    return controller.update_medical_record(record_id, record_data, current_user)

