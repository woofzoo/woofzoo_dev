"""
Lab Test routes for API endpoints.
"""

from fastapi import APIRouter, Depends, status
from typing import List

from app.controllers.lab_test_controller import LabTestController
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.lab_test import LabTestCreate, LabTestResponse, LabTestUpdate

router = APIRouter(prefix="/api/v1/lab-tests", tags=["lab-tests"])


@router.post("/", response_model=LabTestResponse, status_code=status.HTTP_201_CREATED)
def create_lab_test(
    lab_test_data: LabTestCreate,
    current_user: User = Depends(get_current_user),
    controller: LabTestController = Depends()
):
    """Order a new lab test."""
    return controller.create_lab_test(lab_test_data, current_user)


@router.get("/pet/{pet_id}", response_model=List[LabTestResponse])
def get_lab_tests_by_pet(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: LabTestController = Depends()
):
    """Get all lab tests for a pet."""
    return controller.get_lab_tests_by_pet(pet_id, current_user)


@router.get("/pet/{pet_id}/abnormal", response_model=List[LabTestResponse])
def get_abnormal_results(
    pet_id: str,
    current_user: User = Depends(get_current_user),
    controller: LabTestController = Depends()
):
    """Get lab tests with abnormal results."""
    return controller.get_abnormal_results(pet_id, current_user)


@router.put("/{lab_test_id}", response_model=LabTestResponse)
def update_lab_test(
    lab_test_id: str,
    lab_test_data: LabTestUpdate,
    current_user: User = Depends(get_current_user),
    controller: LabTestController = Depends()
):
    """Update a lab test (e.g., add results)."""
    return controller.update_lab_test(lab_test_id, lab_test_data, current_user)

