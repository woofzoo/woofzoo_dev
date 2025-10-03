"""
Doctor Profile Controller - HTTP layer for doctor profile management.
"""

from typing import List
from fastapi import HTTPException, status
import uuid

from app.services.doctor_profile_service import DoctorProfileService
from app.models.user import User
from app.schemas.doctor_profile import (
    DoctorProfileCreate,
    DoctorProfileResponse,
    DoctorProfileUpdate
)


class DoctorProfileController:
    """Controller for doctor profile operations."""
    
    def __init__(self, service: DoctorProfileService):
        self.service = service
    
    def create_doctor_profile(
        self,
        profile_data: DoctorProfileCreate,
        current_user: User
    ) -> DoctorProfileResponse:
        """Create doctor profile for authenticated user."""
        try:
            profile = self.service.create_profile(current_user, profile_data)
            return DoctorProfileResponse.from_orm(profile)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create doctor profile: {str(e)}"
            )
    
    def get_my_doctor_profile(self, current_user: User) -> DoctorProfileResponse:
        """Get authenticated doctor's profile."""
        try:
            profile = self.service.get_profile_by_user_id(current_user.public_id)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doctor profile not found. Please create your profile first."
                )
            return DoctorProfileResponse.from_orm(profile)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve doctor profile: {str(e)}"
            )
    
    def get_doctor_profile(
        self,
        doctor_id: str,
        current_user: User
    ) -> DoctorProfileResponse:
        """Get doctor profile by ID."""
        try:
            doctor_uuid = uuid.UUID(doctor_id)
            profile = self.service.get_profile_by_id(doctor_uuid)
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Doctor profile not found"
                )
            return DoctorProfileResponse.from_orm(profile)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid doctor ID format"
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve doctor profile: {str(e)}"
            )
    
    def update_my_doctor_profile(
        self,
        profile_data: DoctorProfileUpdate,
        current_user: User
    ) -> DoctorProfileResponse:
        """Update authenticated doctor's profile."""
        try:
            profile = self.service.update_profile(current_user, profile_data)
            return DoctorProfileResponse.from_orm(profile)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update doctor profile: {str(e)}"
            )
    
    def search_doctors(
        self,
        specialization: str = None,
        is_verified: bool = None,
        skip: int = 0,
        limit: int = 100,
        current_user: User = None
    ) -> List[DoctorProfileResponse]:
        """Search for doctors."""
        try:
            profiles = self.service.search_doctors(
                specialization=specialization,
                is_verified=is_verified,
                skip=skip,
                limit=limit
            )
            return [DoctorProfileResponse.from_orm(p) for p in profiles]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to search doctors: {str(e)}"
            )

