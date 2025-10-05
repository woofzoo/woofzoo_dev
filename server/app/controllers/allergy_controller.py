"""
Allergy controller for API layer.
"""

from fastapi import HTTPException, status
from loguru import logger

from app.models.user import User
from app.schemas.allergy import AllergyCreate, AllergyResponse, AllergyUpdate
from app.services.allergy_service import AllergyService


class AllergyController:
    """Allergy controller for handling HTTP requests and responses."""
    
    def __init__(self, allergy_service: AllergyService):
        self.allergy_service = allergy_service
    
    def create_allergy(self, allergy_data: AllergyCreate, current_user: User) -> AllergyResponse:
        """Create a new allergy record."""
        try:
            allergy = self.allergy_service.create_allergy(allergy_data, current_user)
            return AllergyResponse.model_validate(allergy)
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.exception("Failed to create allergy")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create allergy")
    
    def get_allergies_by_pet(self, pet_id: str, current_user: User):
        """Get all allergies for a pet."""
        try:
            allergies = self.allergy_service.get_allergies_by_pet(pet_id, current_user)
            return [AllergyResponse.model_validate(a) for a in allergies]
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
    def get_critical_allergies(self, pet_id: str, current_user: User):
        """Get critical allergies for a pet."""
        try:
            allergies = self.allergy_service.get_critical_allergies(pet_id, current_user)
            return [AllergyResponse.model_validate(a) for a in allergies]
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

