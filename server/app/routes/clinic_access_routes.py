"""
Clinic Access routes for API endpoints (OTP workflow).
"""

from fastapi import APIRouter, Depends, status

from app.controllers.clinic_access_controller import ClinicAccessController
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.pet_clinic_access import (
    PetClinicAccessRequest,
    PetClinicAccessGrant,
    PetClinicAccessRevoke,
    PetClinicAccessResponse,
    OTPGenerationResponse
)

router = APIRouter(prefix="/api/v1/clinic-access", tags=["clinic-access"])


@router.post("/request", response_model=OTPGenerationResponse)
def request_clinic_access(
    request_data: PetClinicAccessRequest,
    current_user: User = Depends(get_current_user),
    controller: ClinicAccessController = Depends()
):
    """Request clinic access (generates OTP)."""
    return controller.request_access(request_data, current_user)


@router.post("/grant", response_model=PetClinicAccessResponse, status_code=status.HTTP_201_CREATED)
def grant_clinic_access(
    grant_data: PetClinicAccessGrant,
    current_user: User = Depends(get_current_user),
    controller: ClinicAccessController = Depends()
):
    """Grant clinic access after OTP validation."""
    return controller.grant_access(grant_data, current_user)


@router.post("/revoke")
def revoke_clinic_access(
    revoke_data: PetClinicAccessRevoke,
    current_user: User = Depends(get_current_user),
    controller: ClinicAccessController = Depends()
):
    """Revoke clinic access to pet records."""
    return controller.revoke_access(revoke_data, current_user)

