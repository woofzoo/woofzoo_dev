"""
Doctor-Clinic Association routes for API endpoints.
"""

from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db_session
from app.models.user import User
from app.schemas.doctor_clinic_association import (
    DoctorClinicAssociationCreate,
    DoctorClinicAssociationResponse,
    DoctorClinicAssociationUpdate
)
from app.controllers.doctor_clinic_association_controller import DoctorClinicAssociationController
from app.services.doctor_clinic_association_service import DoctorClinicAssociationService
from app.repositories.doctor_clinic_association import DoctorClinicAssociationRepository
from app.repositories.doctor_profile import DoctorProfileRepository
from app.repositories.clinic_profile import ClinicProfileRepository

router = APIRouter(prefix="/doctor-clinic-associations", tags=["doctor-clinic-associations"])


def get_association_controller(db: Session = Depends(get_db_session)) -> DoctorClinicAssociationController:
    """Dependency injection for association controller."""
    association_repository = DoctorClinicAssociationRepository(db)
    doctor_repository = DoctorProfileRepository(db)
    clinic_repository = ClinicProfileRepository(db)
    service = DoctorClinicAssociationService(
        association_repository,
        doctor_repository,
        clinic_repository
    )
    return DoctorClinicAssociationController(service)


@router.post("/", response_model=DoctorClinicAssociationResponse, status_code=status.HTTP_201_CREATED)
def create_association(
    association_data: DoctorClinicAssociationCreate,
    current_user: User = Depends(get_current_user),
    controller: DoctorClinicAssociationController = Depends(get_association_controller)
):
    """
    Create doctor-clinic association.
    
    Only clinic owners can add doctors to their clinic.
    """
    return controller.create_association(association_data, current_user)


@router.get("/clinic/{clinic_id}/doctors", response_model=List[DoctorClinicAssociationResponse])
def get_clinic_doctors(
    clinic_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    controller: DoctorClinicAssociationController = Depends(get_association_controller)
):
    """Get all doctors associated with a clinic."""
    return controller.get_clinic_doctors(clinic_id, skip, limit, current_user)


@router.get("/doctor/{doctor_id}/clinics", response_model=List[DoctorClinicAssociationResponse])
def get_doctor_clinics(
    doctor_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    controller: DoctorClinicAssociationController = Depends(get_association_controller)
):
    """Get all clinics a doctor is associated with."""
    return controller.get_doctor_clinics(doctor_id, skip, limit, current_user)


@router.put("/{association_id}", response_model=DoctorClinicAssociationResponse)
def update_association(
    association_id: str,
    association_data: DoctorClinicAssociationUpdate,
    current_user: User = Depends(get_current_user),
    controller: DoctorClinicAssociationController = Depends(get_association_controller)
):
    """Update association (e.g., change employment type, deactivate)."""
    return controller.update_association(association_id, association_data, current_user)


@router.delete("/{association_id}", status_code=status.HTTP_200_OK)
def delete_association(
    association_id: str,
    current_user: User = Depends(get_current_user),
    controller: DoctorClinicAssociationController = Depends(get_association_controller)
):
    """
    Delete/deactivate association.
    
    Clinic owner or doctor can end the association.
    """
    return controller.delete_association(association_id, current_user)

