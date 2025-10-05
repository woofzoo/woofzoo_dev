"""
Lab Test controller for API layer.
"""

from fastapi import HTTPException, status
from loguru import logger

from app.models.user import User
from app.schemas.lab_test import LabTestCreate, LabTestResponse, LabTestUpdate
from app.services.lab_test_service import LabTestService


class LabTestController:
    """Lab Test controller for handling HTTP requests and responses."""
    
    def __init__(self, lab_test_service: LabTestService):
        self.lab_test_service = lab_test_service
    
    def create_lab_test(self, lab_test_data: LabTestCreate, current_user: User) -> LabTestResponse:
        """Order a new lab test."""
        try:
            lab_test = self.lab_test_service.create_lab_test(lab_test_data, current_user)
            return LabTestResponse.model_validate(lab_test)
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.exception("Failed to create lab test")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create lab test")
    
    def get_lab_tests_by_pet(self, pet_id: str, current_user: User):
        """Get all lab tests for a pet."""
        try:
            lab_tests = self.lab_test_service.get_lab_tests_by_pet(pet_id, current_user)
            return [LabTestResponse.model_validate(t) for t in lab_tests]
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
    def get_abnormal_results(self, pet_id: str, current_user: User):
        """Get lab tests with abnormal results."""
        try:
            lab_tests = self.lab_test_service.get_abnormal_results(pet_id, current_user)
            return [LabTestResponse.model_validate(t) for t in lab_tests]
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
    def update_lab_test(self, lab_test_id: str, lab_test_data: LabTestUpdate, current_user: User) -> LabTestResponse:
        """Update a lab test (e.g., add results)."""
        try:
            lab_test = self.lab_test_service.update_lab_test(lab_test_id, lab_test_data, current_user)
            if not lab_test:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lab test not found")
            return LabTestResponse.model_validate(lab_test)
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

