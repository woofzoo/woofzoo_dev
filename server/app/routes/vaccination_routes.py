"""
Vaccination routes for API endpoints.
"""

from fastapi import APIRouter, Depends, status
from typing import List

from app.controllers.vaccination_controller import VaccinationController
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.vaccination import VaccinationCreate, VaccinationResponse

router = APIRouter(prefix="/api/v1/vaccinations", tags=["vaccinations"])


@router.post("/", response_model=VaccinationResponse, status_code=status.HTTP_201_CREATED)
def create_vaccination(
    vaccination_data: VaccinationCreate,
    current_user: User = Depends(get_current_user),
    controller: VaccinationController = Depends()
):
    """Create a new vaccination record."""
    return controller.create_vaccination(vaccination_data, current_user)


@router.get("/pet/{pet_id}", response_model=List[VaccinationResponse])
def get_vaccinations_by_pet(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: VaccinationController = Depends()
):
    """Get all vaccinations for a pet."""
    return controller.get_vaccinations_by_pet(pet_id, current_user)


@router.get("/pet/{pet_id}/due", response_model=List[VaccinationResponse])
def get_due_vaccinations(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: VaccinationController = Depends()
):
    """Get vaccinations that are due or overdue."""
    return controller.get_due_vaccinations(pet_id, current_user)

