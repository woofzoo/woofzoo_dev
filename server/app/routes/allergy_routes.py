"""
Allergy routes for API endpoints.
"""

from fastapi import APIRouter, Depends, status
from typing import List

from app.controllers.allergy_controller import AllergyController
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.allergy import AllergyCreate, AllergyResponse

router = APIRouter(prefix="/api/v1/allergies", tags=["allergies"])


@router.post("/", response_model=AllergyResponse, status_code=status.HTTP_201_CREATED)
def create_allergy(
    allergy_data: AllergyCreate,
    current_user: User = Depends(get_current_user),
    controller: AllergyController = Depends()
):
    """Create a new allergy record."""
    return controller.create_allergy(allergy_data, current_user)


@router.get("/pet/{pet_id}", response_model=List[AllergyResponse])
def get_allergies_by_pet(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: AllergyController = Depends()
):
    """Get all allergies for a pet."""
    return controller.get_allergies_by_pet(pet_id, current_user)


@router.get("/pet/{pet_id}/critical", response_model=List[AllergyResponse])
def get_critical_allergies(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: AllergyController = Depends()
):
    """Get critical allergies for a pet."""
    return controller.get_critical_allergies(pet_id, current_user)

