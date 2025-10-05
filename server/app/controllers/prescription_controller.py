"""
Prescription controller for API layer.
"""

from fastapi import HTTPException, status
from loguru import logger

from app.models.user import User
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse, PrescriptionUpdate
from app.services.prescription_service import PrescriptionService


class PrescriptionController:
    """Prescription controller for handling HTTP requests and responses."""
    
    def __init__(self, prescription_service: PrescriptionService):
        self.prescription_service = prescription_service
    
    def create_prescription(self, prescription_data: PrescriptionCreate, current_user: User) -> PrescriptionResponse:
        """Create a new prescription."""
        try:
            prescription = self.prescription_service.create_prescription(prescription_data, current_user)
            return PrescriptionResponse.model_validate(prescription)
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.exception("Failed to create prescription")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create prescription")
    
    def get_prescription(self, prescription_id: str, current_user: User) -> PrescriptionResponse:
        """Get a prescription by ID."""
        try:
            prescription = self.prescription_service.get_prescription(prescription_id, current_user)
            if not prescription:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
            return PrescriptionResponse.model_validate(prescription)
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
    def get_prescriptions_by_pet(self, pet_id: str, current_user: User, skip: int = 0, limit: int = 100):
        """Get all prescriptions for a pet."""
        try:
            prescriptions = self.prescription_service.get_prescriptions_by_pet(pet_id, current_user, skip, limit)
            return [PrescriptionResponse.model_validate(p) for p in prescriptions]
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
    def update_prescription(self, prescription_id: str, prescription_data: PrescriptionUpdate, current_user: User) -> PrescriptionResponse:
        """Update a prescription."""
        try:
            prescription = self.prescription_service.update_prescription(prescription_id, prescription_data, current_user)
            if not prescription:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
            return PrescriptionResponse.model_validate(prescription)
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

