"""
Lab Test routes for API endpoints.
"""

from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session

from app.controllers.lab_test_controller import LabTestController
from app.services.lab_test_service import LabTestService
from app.services.permission_service import PermissionService
from app.repositories.lab_test import LabTestRepository
from app.repositories.pet import PetRepository
from app.repositories.family_member import FamilyMemberRepository
from app.repositories.pet_clinic_access import PetClinicAccessRepository
from app.dependencies import get_current_user, get_db_session
from app.models.user import User
from app.schemas.lab_test import LabTestCreate, LabTestResponse, LabTestUpdate

router = APIRouter(prefix="/api/v1/lab-tests", tags=["lab-tests"])


def get_lab_test_controller(db: Session = Depends(get_db_session)) -> LabTestController:
    """Dependency injection for lab test controller."""
    lab_test_repo = LabTestRepository(db)
    pet_repo = PetRepository(db)
    family_member_repo = FamilyMemberRepository(db)
    clinic_access_repo = PetClinicAccessRepository(db)
    permission_service = PermissionService(db, pet_repo, family_member_repo, clinic_access_repo)
    service = LabTestService(lab_test_repo, permission_service)
    return LabTestController(service)


@router.post("/", response_model=LabTestResponse, status_code=status.HTTP_201_CREATED)
def create_lab_test(
    lab_test_data: LabTestCreate,
    current_user: User = Depends(get_current_user),
    controller: LabTestController = Depends(get_lab_test_controller)
):
    """Order a new lab test."""
    return controller.create_lab_test(lab_test_data, current_user)


@router.get("/pet/{pet_id}", response_model=List[LabTestResponse])
def get_lab_tests_by_pet(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: LabTestController = Depends(get_lab_test_controller)
):
    """Get all lab tests for a pet."""
    return controller.get_lab_tests_by_pet(pet_id, current_user)


@router.get("/pet/{pet_id}/abnormal", response_model=List[LabTestResponse])
def get_abnormal_results(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: LabTestController = Depends(get_lab_test_controller)
):
    """Get lab tests with abnormal results."""
    return controller.get_abnormal_results(pet_id, current_user)


@router.put("/{lab_test_id}", response_model=LabTestResponse)
def update_lab_test(
    lab_test_id: str,
    lab_test_data: LabTestUpdate,
    current_user: User = Depends(get_current_user),
    controller: LabTestController = Depends(get_lab_test_controller)
):
    """Update a lab test (e.g., add results)."""
    return controller.update_lab_test(lab_test_id, lab_test_data, current_user)

