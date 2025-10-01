"""
Vaccination controller for API layer.
"""

from fastapi import HTTPException, status
from loguru import logger

from app.models.user import User
from app.schemas.vaccination import VaccinationCreate, VaccinationResponse, VaccinationUpdate
from app.services.vaccination_service import VaccinationService


class VaccinationController:
    """Vaccination controller for handling HTTP requests and responses."""
    
    def __init__(self, vaccination_service: VaccinationService):
        self.vaccination_service = vaccination_service
    
    def create_vaccination(self, vaccination_data: VaccinationCreate, current_user: User) -> VaccinationResponse:
        """Create a new vaccination record."""
        try:
            vaccination = self.vaccination_service.create_vaccination(vaccination_data, current_user)
            return VaccinationResponse.model_validate(vaccination)
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.exception("Failed to create vaccination")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create vaccination")
    
    def get_vaccinations_by_pet(self, pet_id: str, current_user: User):
        """Get all vaccinations for a pet."""
        try:
            vaccinations = self.vaccination_service.get_vaccinations_by_pet(pet_id, current_user)
            return [VaccinationResponse.model_validate(v) for v in vaccinations]
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
    def get_due_vaccinations(self, pet_id: str, current_user: User):
        """Get vaccinations that are due or overdue."""
        try:
            vaccinations = self.vaccination_service.get_due_vaccinations(pet_id, current_user)
            return [VaccinationResponse.model_validate(v) for v in vaccinations]
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

