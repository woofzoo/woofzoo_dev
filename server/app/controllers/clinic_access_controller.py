"""
Clinic Access controller for API layer.
"""

from fastapi import HTTPException, status
from loguru import logger

from app.models.user import User
from app.schemas.pet_clinic_access import (
    PetClinicAccessRequest, 
    PetClinicAccessGrant,
    PetClinicAccessRevoke,
    PetClinicAccessResponse,
    OTPGenerationResponse
)
from app.services.clinic_access_service import ClinicAccessService


class ClinicAccessController:
    """Clinic Access controller for OTP-based access control."""
    
    def __init__(self, clinic_access_service: ClinicAccessService):
        self.clinic_access_service = clinic_access_service
    
    def request_access(self, request_data: PetClinicAccessRequest, current_user: User) -> OTPGenerationResponse:
        """Request clinic access (generates OTP)."""
        try:
            result = self.clinic_access_service.request_access(request_data, current_user)
            return OTPGenerationResponse(**result)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.exception("Failed to request clinic access")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to request access")
    
    def grant_access(self, grant_data: PetClinicAccessGrant, current_user: User) -> PetClinicAccessResponse:
        """Grant clinic access after OTP validation."""
        try:
            access = self.clinic_access_service.grant_access(grant_data, current_user)
            return PetClinicAccessResponse.model_validate(access)
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.exception("Failed to grant clinic access")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to grant access")
    
    def revoke_access(self, revoke_data: PetClinicAccessRevoke, current_user: User) -> dict:
        """Revoke clinic access."""
        try:
            success = self.clinic_access_service.revoke_access(revoke_data.access_id, current_user)
            if not success:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Access record not found")
            return {"message": "Access revoked successfully"}
        except PermissionError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

