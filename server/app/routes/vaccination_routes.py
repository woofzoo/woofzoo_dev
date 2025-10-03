"""
Vaccination routes for API endpoints.
"""

from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.controllers.vaccination_controller import VaccinationController
from app.services.vaccination_service import VaccinationService
from app.services.permission_service import PermissionService
from app.repositories.vaccination import VaccinationRepository
from app.repositories.pet import PetRepository
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from app.dependencies import get_current_user, get_db_session
from app.models.user import User
from app.schemas.vaccination import VaccinationCreate, VaccinationResponse

router = APIRouter(prefix="/api/v1/vaccinations", tags=["vaccinations"])


def get_vaccination_controller(db: Session = Depends(get_db_session)) -> VaccinationController:
    """Dependency injection for vaccination controller."""
    vaccination_repo = VaccinationRepository(db)
    pet_repo = PetRepository(db)
    clinic_access_repo = PetClinicAccessRepository(db)
    permission_service = PermissionService(pet_repo, clinic_access_repo)
    service = VaccinationService(vaccination_repo, permission_service)
    return VaccinationController(service)


@router.post("/", response_model=VaccinationResponse, status_code=status.HTTP_201_CREATED)
def create_vaccination(
    vaccination_data: VaccinationCreate,
    current_user: User = Depends(get_current_user),
    controller: VaccinationController = Depends(get_vaccination_controller)
):
    """Create a new vaccination record."""
    return controller.create_vaccination(vaccination_data, current_user)


@router.get("/pet/{pet_id}", response_model=List[VaccinationResponse])
def get_vaccinations_by_pet(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: VaccinationController = Depends(get_vaccination_controller)
):
    """Get all vaccinations for a pet."""
    return controller.get_vaccinations_by_pet(pet_id, current_user)


@router.get("/pet/{pet_id}/due", response_model=List[VaccinationResponse])
def get_due_vaccinations(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: VaccinationController = Depends(get_vaccination_controller)
):
    """Get vaccinations that are due or overdue."""
    return controller.get_due_vaccinations(pet_id, current_user)

