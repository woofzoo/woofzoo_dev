"""
Allergy routes for API endpoints.
"""

from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.controllers.allergy_controller import AllergyController
from app.services.allergy_service import AllergyService
from app.services.permission_service import PermissionService
from app.repositories.allergy import AllergyRepository
from app.repositories.pet import PetRepository
from app.repositories.family_member import FamilyMemberRepository
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from app.dependencies import get_current_user, get_db_session
from app.models.user import User
from app.schemas.allergy import AllergyCreate, AllergyResponse

router = APIRouter(prefix="/api/v1/allergies", tags=["allergies"])


def get_allergy_controller(db: Session = Depends(get_db_session)) -> AllergyController:
    """Dependency injection for allergy controller."""
    allergy_repo = AllergyRepository(db)
    pet_repo = PetRepository(db)
    family_member_repo = FamilyMemberRepository(db)
    clinic_access_repo = PetClinicAccessRepository(db)
    permission_service = PermissionService(db, pet_repo, family_member_repo, clinic_access_repo)
    service = AllergyService(allergy_repo, permission_service)
    return AllergyController(service)


@router.post("/", response_model=AllergyResponse, status_code=status.HTTP_201_CREATED)
def create_allergy(
    allergy_data: AllergyCreate,
    current_user: User = Depends(get_current_user),
    controller: AllergyController = Depends(get_allergy_controller)
):
    """Create a new allergy record."""
    return controller.create_allergy(allergy_data, current_user)


@router.get("/pet/{pet_id}", response_model=List[AllergyResponse])
def get_allergies_by_pet(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: AllergyController = Depends(get_allergy_controller)
):
    """Get all allergies for a pet."""
    return controller.get_allergies_by_pet(pet_id, current_user)


@router.get("/pet/{pet_id}/critical", response_model=List[AllergyResponse])
def get_critical_allergies(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: AllergyController = Depends(get_allergy_controller)
):
    """Get critical allergies for a pet."""
    return controller.get_critical_allergies(pet_id, current_user)

