"""
Clinic Profile Controller - HTTP layer for clinic profile management.
"""

from typing import List
from fastapi import HTTPException, status
import uuid

from app.services.clinic_profile_service import ClinicProfileService
from app.models.user import User
from app.schemas.clinic_profile import (
    ClinicProfileCreate,
    ClinicProfileResponse,
    ClinicProfileUpdate
)


class ClinicProfileController:
    """Controller for clinic profile operations."""
    
    def __init__(self, service: ClinicProfileService):
        self.service = service
    
    def create_clinic_profile(
        self,
        profile_data: ClinicProfileCreate,
        current_user: User
    ) -> ClinicProfileResponse:
        """Create clinic profile for authenticated user."""
        try:
            profile = self.service.create_profile(current_user, profile_data)
            return ClinicProfileResponse.model_validate(profile)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create clinic profile: {str(e)}"
            )
    
    def get_my_clinic_profile(self, current_user: User) -> ClinicProfileResponse:
        """Get authenticated clinic owner's profile."""
        try:
            profile = self.service.get_profile_by_user_id(current_user.public_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Clinic profile not found. Please create your profile first."
                )
            return ClinicProfileResponse.model_validate(profile)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve clinic profile: {str(e)}"
            )
    
    def get_clinic_profile(
        self,
        clinic_id: str,
        current_user: User = None
    ) -> ClinicProfileResponse:
        """Get clinic profile by ID (public endpoint)."""
        try:
            clinic_uuid = uuid.UUID(clinic_id)
            profile = self.service.get_profile_by_id(clinic_uuid)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Clinic profile not found"
                )
            return ClinicProfileResponse.model_validate(profile)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid clinic ID format"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve clinic profile: {str(e)}"
            )
    
    def update_my_clinic_profile(
        self,
        profile_data: ClinicProfileUpdate,
        current_user: User
    ) -> ClinicProfileResponse:
        """Update authenticated clinic owner's profile."""
        try:
            profile = self.service.update_profile(current_user, profile_data)
            return ClinicProfileResponse.model_validate(profile)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update clinic profile: {str(e)}"
            )
    
    def search_clinics(
        self,
        clinic_name: str = None,
        is_verified: bool = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ClinicProfileResponse]:
        """Search for clinics (public endpoint)."""
        try:
            profiles = self.service.search_clinics(
                clinic_name=clinic_name,
                is_verified=is_verified,
                skip=skip,
                limit=limit
            )
            return [ClinicProfileResponse.model_validate(p) for p in profiles]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to search clinics: {str(e)}"
            )

