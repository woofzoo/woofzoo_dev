"""
Clinic Profile routes for API endpoints.
"""

from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db_session
from app.models.user import User
from app.schemas.clinic_profile import (
    ClinicProfileCreate,
    ClinicProfileResponse,
    ClinicProfileUpdate
)
from app.controllers.clinic_profile_controller import ClinicProfileController
from app.services.clinic_profile_service import ClinicProfileService
from app.repositories.clinic_profile import ClinicProfileRepository

router = APIRouter(prefix="/clinic-profiles", tags=["clinic-profiles"])


def get_clinic_profile_controller(db: Session = Depends(get_db_session)) -> ClinicProfileController:
    """Dependency injection for clinic profile controller."""
    repository = ClinicProfileRepository(db)
    service = ClinicProfileService(repository)
    return ClinicProfileController(service)


@router.post("/", response_model=ClinicProfileResponse, status_code=status.HTTP_201_CREATED)
def create_clinic_profile(
    profile_data: ClinicProfileCreate,
    current_user: User = Depends(get_current_user),
    controller: ClinicProfileController = Depends(get_clinic_profile_controller)
):
    """
    Create clinic profile for authenticated user.
    
    User must have 'clinic_owner' role.
    Creates the clinic_profiles entry that links to the user account.
    """
    return controller.create_clinic_profile(profile_data, current_user)


@router.get("/me", response_model=ClinicProfileResponse)
def get_my_clinic_profile(
    current_user: User = Depends(get_current_user),
    controller: ClinicProfileController = Depends(get_clinic_profile_controller)
):
    """Get the authenticated clinic owner's profile."""
    return controller.get_my_clinic_profile(current_user)


@router.get("/{clinic_id}", response_model=ClinicProfileResponse)
def get_clinic_profile(
    clinic_id: str,
    current_user: User = Depends(get_current_user),
    controller: ClinicProfileController = Depends(get_clinic_profile_controller)
):
    """Get a clinic profile by ID (public information)."""
    return controller.get_clinic_profile(clinic_id, current_user)


@router.put("/me", response_model=ClinicProfileResponse)
def update_my_clinic_profile(
    profile_data: ClinicProfileUpdate,
    current_user: User = Depends(get_current_user),
    controller: ClinicProfileController = Depends(get_clinic_profile_controller)
):
    """Update the authenticated clinic owner's profile."""
    return controller.update_my_clinic_profile(profile_data, current_user)


@router.get("/", response_model=List[ClinicProfileResponse])
def search_clinics(
    clinic_name: str = Query(None, description="Search by name"),
    is_verified: bool = Query(None, description="Filter by verification status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    controller: ClinicProfileController = Depends(get_clinic_profile_controller)
):
    """Search for clinics (public endpoint for pet owners to find clinics)."""
    return controller.search_clinics(clinic_name, is_verified, skip, limit)

