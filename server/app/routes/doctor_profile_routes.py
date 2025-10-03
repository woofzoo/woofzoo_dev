"""
Doctor Profile routes for API endpoints.
"""

from fastapi import APIRouter, Depends, Query, status
from typing import List

from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.doctor_profile import (
    DoctorProfileCreate,
    DoctorProfileResponse,
    DoctorProfileUpdate
)

router = APIRouter(prefix="/api/v1/doctor-profiles", tags=["doctor-profiles"])


@router.post("/", response_model=DoctorProfileResponse, status_code=status.HTTP_201_CREATED)
def create_doctor_profile(
    profile_data: DoctorProfileCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create doctor profile for authenticated user.
    
    User must have 'doctor' role.
    Creates the doctor_profiles entry that links to the user account.
    """
    # TODO: Implement in controller
    pass


@router.get("/me", response_model=DoctorProfileResponse)
def get_my_doctor_profile(
    current_user: User = Depends(get_current_user)
):
    """Get the authenticated doctor's profile."""
    # TODO: Implement in controller
    pass


@router.get("/{doctor_id}", response_model=DoctorProfileResponse)
def get_doctor_profile(
    doctor_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a doctor profile by ID."""
    # TODO: Implement in controller
    pass


@router.put("/me", response_model=DoctorProfileResponse)
def update_my_doctor_profile(
    profile_data: DoctorProfileUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update the authenticated doctor's profile."""
    # TODO: Implement in controller
    pass


@router.get("/", response_model=List[DoctorProfileResponse])
def search_doctors(
    specialization: str = Query(None, description="Filter by specialization"),
    is_verified: bool = Query(None, description="Filter by verification status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    current_user: User = Depends(get_current_user)
):
    """Search for doctors (for clinic owners to find doctors to associate)."""
    # TODO: Implement in controller
    pass

