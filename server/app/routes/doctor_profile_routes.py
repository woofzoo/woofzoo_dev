"""
Doctor Profile routes for API endpoints.
"""

from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db_session
from app.models.user import User
from app.schemas.doctor_profile import (
    DoctorProfileCreate,
    DoctorProfileResponse,
    DoctorProfileUpdate
)
from app.controllers.doctor_profile_controller import DoctorProfileController
from app.services.doctor_profile_service import DoctorProfileService
from app.repositories.doctor_profile import DoctorProfileRepository

router = APIRouter(prefix="/api/v1/doctor-profiles", tags=["doctor-profiles"])


def get_doctor_profile_controller(db: Session = Depends(get_db_session)) -> DoctorProfileController:
    """Dependency injection for doctor profile controller."""
    repository = DoctorProfileRepository(db)
    service = DoctorProfileService(repository)
    return DoctorProfileController(service)


@router.post("/", response_model=DoctorProfileResponse, status_code=status.HTTP_201_CREATED)
def create_doctor_profile(
    profile_data: DoctorProfileCreate,
    current_user: User = Depends(get_current_user),
    controller: DoctorProfileController = Depends(get_doctor_profile_controller)
):
    """
    Create doctor profile for authenticated user.
    
    User must have 'doctor' role.
    Creates the doctor_profiles entry that links to the user account.
    """
    return controller.create_doctor_profile(profile_data, current_user)


@router.get("/me", response_model=DoctorProfileResponse)
def get_my_doctor_profile(
    current_user: User = Depends(get_current_user),
    controller: DoctorProfileController = Depends(get_doctor_profile_controller)
):
    """Get the authenticated doctor's profile."""
    return controller.get_my_doctor_profile(current_user)


@router.get("/{doctor_id}", response_model=DoctorProfileResponse)
def get_doctor_profile(
    doctor_id: str,
    current_user: User = Depends(get_current_user),
    controller: DoctorProfileController = Depends(get_doctor_profile_controller)
):
    """Get a doctor profile by ID."""
    return controller.get_doctor_profile(doctor_id, current_user)


@router.put("/me", response_model=DoctorProfileResponse)
def update_my_doctor_profile(
    profile_data: DoctorProfileUpdate,
    current_user: User = Depends(get_current_user),
    controller: DoctorProfileController = Depends(get_doctor_profile_controller)
):
    """Update the authenticated doctor's profile."""
    return controller.update_my_doctor_profile(profile_data, current_user)


@router.get("/", response_model=List[DoctorProfileResponse])
def search_doctors(
    specialization: str = Query(None, description="Filter by specialization"),
    is_verified: bool = Query(None, description="Filter by verification status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    controller: DoctorProfileController = Depends(get_doctor_profile_controller)
):
    """Search for doctors (for clinic owners to find doctors to associate)."""
    return controller.search_doctors(specialization, is_verified, skip, limit, current_user)

