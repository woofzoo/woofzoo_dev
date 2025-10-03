"""
Doctor-Clinic Association routes for API endpoints.
"""

from fastapi import APIRouter, Depends, status
from typing import List

from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.doctor_clinic_association import (
    DoctorClinicAssociationCreate,
    DoctorClinicAssociationResponse,
    DoctorClinicAssociationUpdate
)

router = APIRouter(prefix="/api/v1/doctor-clinic-associations", tags=["doctor-clinic-associations"])


@router.post("/", response_model=DoctorClinicAssociationResponse, status_code=status.HTTP_201_CREATED)
def create_association(
    association_data: DoctorClinicAssociationCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create doctor-clinic association.
    
    Only clinic owners can add doctors to their clinic.
    Doctor must approve the association.
    """
    # TODO: Implement in controller
    pass


@router.get("/clinic/{clinic_id}/doctors", response_model=List[DoctorClinicAssociationResponse])
def get_clinic_doctors(
    clinic_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all doctors associated with a clinic."""
    # TODO: Implement in controller
    pass


@router.get("/doctor/{doctor_id}/clinics", response_model=List[DoctorClinicAssociationResponse])
def get_doctor_clinics(
    doctor_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all clinics a doctor is associated with."""
    # TODO: Implement in controller
    pass


@router.put("/{association_id}", response_model=DoctorClinicAssociationResponse)
def update_association(
    association_id: str,
    association_data: DoctorClinicAssociationUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update association (e.g., change employment type, deactivate)."""
    # TODO: Implement in controller
    pass


@router.delete("/{association_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_association(
    association_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Delete/deactivate association.
    
    Clinic owner or doctor can end the association.
    """
    # TODO: Implement in controller
    pass

