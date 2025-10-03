"""
Prescription routes for API endpoints.
"""

from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.orm import Session

from app.controllers.prescription_controller import PrescriptionController
from app.services.prescription_service import PrescriptionService
from app.services.permission_service import PermissionService
from app.repositories.prescription import PrescriptionRepository
from app.repositories.pet import PetRepository
from app.repositories.family_member import FamilyMemberRepository
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from app.dependencies import get_current_user, get_db_session
from app.models.user import User
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse, PrescriptionUpdate

router = APIRouter(prefix="/api/v1/prescriptions", tags=["prescriptions"])


def get_prescription_controller(db: Session = Depends(get_db_session)) -> PrescriptionController:
    """Dependency injection for prescription controller."""
    prescription_repo = PrescriptionRepository(db)
    pet_repo = PetRepository(db)
    family_member_repo = FamilyMemberRepository(db)
    clinic_access_repo = PetClinicAccessRepository(db)
    permission_service = PermissionService(db, pet_repo, family_member_repo, clinic_access_repo)
    service = PrescriptionService(prescription_repo, permission_service)
    return PrescriptionController(service)


@router.post("/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
def create_prescription(
    prescription_data: PrescriptionCreate,
    current_user: User = Depends(get_current_user),
    controller: PrescriptionController = Depends(get_prescription_controller)
):
    """Create a new prescription."""
    return controller.create_prescription(prescription_data, current_user)


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: str,
    current_user: User = Depends(get_current_user),
    controller: PrescriptionController = Depends(get_prescription_controller)
):
    """Get a prescription by ID."""
    return controller.get_prescription(prescription_id, current_user)


@router.get("/pet/{pet_id}", response_model=List[PrescriptionResponse])
def get_prescriptions_by_pet(
    pet_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    controller: PrescriptionController = Depends(get_prescription_controller)
):
    """Get all prescriptions for a pet."""
    return controller.get_prescriptions_by_pet(pet_id, current_user, skip, limit)


@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: str,
    prescription_data: PrescriptionUpdate,
    current_user: User = Depends(get_current_user),
    controller: PrescriptionController = Depends(get_prescription_controller)
):
    """Update a prescription."""
    return controller.update_prescription(prescription_id, prescription_data, current_user)

