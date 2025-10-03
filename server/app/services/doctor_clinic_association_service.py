"""
Doctor-Clinic Association Service - Business logic for managing doctor-clinic relationships.
"""

from typing import List, Optional
import uuid
from datetime import datetime

from app.repositories.doctor_clinic_association import DoctorClinicAssociationRepository
from app.repositories.doctor_profile import DoctorProfileRepository
from app.repositories.clinic_profile import ClinicProfileRepository
from app.models.doctor_clinic_association import DoctorClinicAssociation, EmploymentType
from app.models.user import User
from app.schemas.doctor_clinic_association import (
    DoctorClinicAssociationCreate,
    DoctorClinicAssociationUpdate
)


class DoctorClinicAssociationService:
    """Service for managing doctor-clinic associations."""
    
    def __init__(
        self,
        association_repository: DoctorClinicAssociationRepository,
        doctor_repository: DoctorProfileRepository,
        clinic_repository: ClinicProfileRepository
    ):
        self.association_repository = association_repository
        self.doctor_repository = doctor_repository
        self.clinic_repository = clinic_repository
    
    def create_association(
        self,
        user: User,
        association_data: DoctorClinicAssociationCreate
    ) -> DoctorClinicAssociation:
        """
        Create doctor-clinic association.
        
        Only clinic owners can add doctors to their clinic.
        """
        # Verify user owns the clinic
        clinic = self.clinic_repository.get_by_id(association_data.clinic_id)
        if not clinic:
            raise ValueError("Clinic not found")
        
        if clinic.user_id != user.public_id:
            raise PermissionError("Only clinic owner can add doctors to their clinic")
        
        # Verify doctor profile exists
        doctor = self.doctor_repository.get_by_id(association_data.doctor_id)
        if not doctor:
            raise ValueError("Doctor profile not found")
        
        # Check if association already exists
        existing = self.association_repository.get_by_doctor_and_clinic(
            association_data.doctor_id,
            association_data.clinic_id
        )
        if existing:
            if existing.is_active:
                raise ValueError("Doctor is already associated with this clinic")
            else:
                # Reactivate existing association
                existing.is_active = True
                existing.employment_type = association_data.employment_type
                existing.joined_at = datetime.utcnow()
                return self.association_repository.update(existing)
        
        # Create new association
        association = DoctorClinicAssociation(
            id=uuid.uuid4(),
            doctor_id=association_data.doctor_id,
            clinic_id=association_data.clinic_id,
            employment_type=EmploymentType(association_data.employment_type),
            is_active=True,
            joined_at=datetime.utcnow()
        )
        
        return self.association_repository.save(association)
    
    def get_clinic_doctors(
        self,
        clinic_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[DoctorClinicAssociation]:
        """Get all doctors associated with a clinic."""
        return self.association_repository.get_by_clinic_id(
            clinic_id,
            skip=skip,
            limit=limit
        )
    
    def get_doctor_clinics(
        self,
        doctor_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[DoctorClinicAssociation]:
        """Get all clinics a doctor is associated with."""
        return self.association_repository.get_by_doctor_id(
            doctor_id,
            skip=skip,
            limit=limit
        )
    
    def update_association(
        self,
        user: User,
        association_id: uuid.UUID,
        update_data: DoctorClinicAssociationUpdate
    ) -> DoctorClinicAssociation:
        """
        Update association.
        
        Only clinic owner can update the association.
        """
        association = self.association_repository.get_by_id(association_id)
        if not association:
            raise ValueError("Association not found")
        
        # Verify user owns the clinic
        clinic = self.clinic_repository.get_by_id(association.clinic_id)
        if clinic.user_id != user.public_id:
            raise PermissionError("Only clinic owner can update associations")
        
        # Update fields
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(association, field, value)
        
        return self.association_repository.update(association)
    
    def delete_association(
        self,
        user: User,
        association_id: uuid.UUID
    ) -> None:
        """
        Delete/deactivate association.
        
        Either clinic owner or the doctor can end the association.
        """
        association = self.association_repository.get_by_id(association_id)
        if not association:
            raise ValueError("Association not found")
        
        # Check permission: either clinic owner or the doctor
        clinic = self.clinic_repository.get_by_id(association.clinic_id)
        doctor = self.doctor_repository.get_by_id(association.doctor_id)
        
        is_clinic_owner = clinic.user_id == user.public_id
        is_doctor = doctor.user_id == user.public_id
        
        if not (is_clinic_owner or is_doctor):
            raise PermissionError("Only clinic owner or doctor can end association")
        
        # Soft delete - mark as inactive
        association.is_active = False
        self.association_repository.update(association)
    
    def verify_doctor_works_at_clinic(
        self,
        doctor_id: uuid.UUID,
        clinic_id: uuid.UUID
    ) -> bool:
        """Check if doctor currently works at clinic (active association)."""
        associations = self.association_repository.get_active_by_doctor_id(doctor_id)
        return any(a.clinic_id == clinic_id for a in associations)

