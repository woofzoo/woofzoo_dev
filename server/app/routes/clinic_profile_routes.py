"""
Clinic Profile routes for API endpoints.
"""

from fastapi import APIRouter, Depends, Query, status
from typing import List

from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.clinic_profile import (
    ClinicProfileCreate,
    ClinicProfileResponse,
    ClinicProfileUpdate
)

router = APIRouter(prefix="/api/v1/clinic-profiles", tags=["clinic-profiles"])


@router.post("/", response_model=ClinicProfileResponse, status_code=status.HTTP_201_CREATED)
def create_clinic_profile(
    profile_data: ClinicProfileCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create clinic profile for authenticated user.
    
    User must have 'clinic_owner' role.
    Creates the clinic_profiles entry that links to the user account.
    """
    # TODO: Implement in controller
    pass


@router.get("/me", response_model=ClinicProfileResponse)
def get_my_clinic_profile(
    current_user: User = Depends(get_current_user)
):
    """Get the authenticated clinic owner's profile."""
    # TODO: Implement in controller
    pass


@router.get("/{clinic_id}", response_model=ClinicProfileResponse)
def get_clinic_profile(
    clinic_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a clinic profile by ID (public information)."""
    # TODO: Implement in controller
    pass


@router.put("/me", response_model=ClinicProfileResponse)
def update_my_clinic_profile(
    profile_data: ClinicProfileUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update the authenticated clinic owner's profile."""
    # TODO: Implement in controller
    pass


@router.get("/", response_model=List[ClinicProfileResponse])
def search_clinics(
    clinic_name: str = Query(None, description="Search by name"),
    is_verified: bool = Query(None, description="Filter by verification status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000)
):
    """Search for clinics (public endpoint for pet owners to find clinics)."""
    # TODO: Implement in controller
    pass

