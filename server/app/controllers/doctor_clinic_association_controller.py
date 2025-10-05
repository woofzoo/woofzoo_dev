"""
Doctor-Clinic Association Controller - HTTP layer for association management.
"""

from typing import List
from fastapi import HTTPException, status
import uuid

from app.services.doctor_clinic_association_service import DoctorClinicAssociationService
from app.models.user import User
from app.schemas.doctor_clinic_association import (
    DoctorClinicAssociationCreate,
    DoctorClinicAssociationResponse,
    DoctorClinicAssociationUpdate
)


class DoctorClinicAssociationController:
    """Controller for doctor-clinic association operations."""
    
    def __init__(self, service: DoctorClinicAssociationService):
        self.service = service
    
    def create_association(
        self,
        association_data: DoctorClinicAssociationCreate,
        current_user: User
    ) -> DoctorClinicAssociationResponse:
        """Create doctor-clinic association."""
        try:
            association = self.service.create_association(current_user, association_data)
            return DoctorClinicAssociationResponse.model_validate(association)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create association: {str(e)}"
            )
    
    def get_clinic_doctors(
        self,
        clinic_id: str,
        skip: int = 0,
        limit: int = 100,
        current_user: User = None
    ) -> List[DoctorClinicAssociationResponse]:
        """Get all doctors associated with a clinic."""
        try:
            clinic_uuid = uuid.UUID(clinic_id)
            associations = self.service.get_clinic_doctors(
                clinic_uuid,
                skip=skip,
                limit=limit
            )
            return [DoctorClinicAssociationResponse.model_validate(a) for a in associations]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid clinic ID format"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve clinic doctors: {str(e)}"
            )
    
    def get_doctor_clinics(
        self,
        doctor_id: str,
        skip: int = 0,
        limit: int = 100,
        current_user: User = None
    ) -> List[DoctorClinicAssociationResponse]:
        """Get all clinics a doctor is associated with."""
        try:
            doctor_uuid = uuid.UUID(doctor_id)
            associations = self.service.get_doctor_clinics(
                doctor_uuid,
                skip=skip,
                limit=limit
            )
            return [DoctorClinicAssociationResponse.model_validate(a) for a in associations]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid doctor ID format"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve doctor clinics: {str(e)}"
            )
    
    def update_association(
        self,
        association_id: str,
        association_data: DoctorClinicAssociationUpdate,
        current_user: User
    ) -> DoctorClinicAssociationResponse:
        """Update association."""
        try:
            assoc_uuid = uuid.UUID(association_id)
            association = self.service.update_association(
                current_user,
                assoc_uuid,
                association_data
            )
            return DoctorClinicAssociationResponse.model_validate(association)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update association: {str(e)}"
            )
    
    def delete_association(
        self,
        association_id: str,
        current_user: User
    ) -> dict:
        """Delete/deactivate association."""
        try:
            assoc_uuid = uuid.UUID(association_id)
            self.service.delete_association(current_user, assoc_uuid)
            return {"message": "Association successfully ended"}
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete association: {str(e)}"
            )

