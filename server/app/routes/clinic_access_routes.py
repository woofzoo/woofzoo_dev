"""
Clinic Access routes for API endpoints (OTP workflow).
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.clinic_access_controller import ClinicAccessController
from app.services.clinic_access_service import ClinicAccessService
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from app.repositories.pet import PetRepository
from app.dependencies import get_current_user, get_db_session
from app.models.user import User
from app.schemas.pet_clinic_access import (
    PetClinicAccessRequest,
    PetClinicAccessGrant,
    PetClinicAccessRevoke,
    PetClinicAccessResponse,
    OTPGenerationResponse
)

router = APIRouter(prefix="/clinic-access", tags=["clinic-access"])


def get_clinic_access_controller(db: Session = Depends(get_db_session)) -> ClinicAccessController:
    """Dependency injection for clinic access controller."""
    clinic_access_repo = PetClinicAccessRepository(db)
    pet_repo = PetRepository(db)
    service = ClinicAccessService(db, clinic_access_repo, pet_repo)
    return ClinicAccessController(service)


@router.post("/request", response_model=OTPGenerationResponse)
def request_clinic_access(
    request_data: PetClinicAccessRequest,
    current_user: User = Depends(get_current_user),
    controller: ClinicAccessController = Depends(get_clinic_access_controller)
):
    """Request clinic access (generates OTP)."""
    return controller.request_access(request_data, current_user)


@router.post("/grant", response_model=PetClinicAccessResponse, status_code=status.HTTP_201_CREATED)
def grant_clinic_access(
    grant_data: PetClinicAccessGrant,
    current_user: User = Depends(get_current_user),
    controller: ClinicAccessController = Depends(get_clinic_access_controller)
):
    """Grant clinic access after OTP validation."""
    return controller.grant_access(grant_data, current_user)


@router.post("/revoke")
def revoke_clinic_access(
    revoke_data: PetClinicAccessRevoke,
    current_user: User = Depends(get_current_user),
    controller: ClinicAccessController = Depends(get_clinic_access_controller)
):
    """Revoke clinic access to pet records."""
    return controller.revoke_access(revoke_data, current_user)

