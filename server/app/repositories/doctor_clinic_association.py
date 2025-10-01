"""
Doctor Clinic Association repository for database operations.

This module provides the DoctorClinicAssociationRepository class for managing
doctor-clinic relationships.
"""

from typing import Optional, List
import uuid

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.models.doctor_clinic_association import DoctorClinicAssociation, EmploymentType
from app.repositories.base import BaseRepository


class DoctorClinicAssociationRepository(BaseRepository[DoctorClinicAssociation]):
    """
    Doctor Clinic Association repository for managing doctor-clinic relationships.
    
    This class extends BaseRepository to provide association-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the doctor clinic association repository."""
        super().__init__(DoctorClinicAssociation, session)
    
    def get_by_doctor_id(self, doctor_id: str) -> List[DoctorClinicAssociation]:
        """
        Get all clinic associations for a doctor.
        
        Args:
            doctor_id: Doctor's ID
            
        Returns:
            List of DoctorClinicAssociation instances
        """
        try:
            doctor_id_uuid = uuid.UUID(doctor_id)
            result = self.session.execute(
                select(DoctorClinicAssociation)
                .where(DoctorClinicAssociation.doctor_id == doctor_id_uuid)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_active_by_doctor_id(self, doctor_id: str) -> List[DoctorClinicAssociation]:
        """
        Get active clinic associations for a doctor.
        
        Args:
            doctor_id: Doctor's ID
            
        Returns:
            List of active DoctorClinicAssociation instances
        """
        try:
            doctor_id_uuid = uuid.UUID(doctor_id)
            result = self.session.execute(
                select(DoctorClinicAssociation)
                .where(
                    and_(
                        DoctorClinicAssociation.doctor_id == doctor_id_uuid,
                        DoctorClinicAssociation.is_active == True
                    )
                )
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_clinic_id(self, clinic_id: str) -> List[DoctorClinicAssociation]:
        """
        Get all doctor associations for a clinic.
        
        Args:
            clinic_id: Clinic's ID
            
        Returns:
            List of DoctorClinicAssociation instances
        """
        try:
            clinic_id_uuid = uuid.UUID(clinic_id)
            result = self.session.execute(
                select(DoctorClinicAssociation)
                .where(DoctorClinicAssociation.clinic_id == clinic_id_uuid)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_active_by_clinic_id(self, clinic_id: str) -> List[DoctorClinicAssociation]:
        """
        Get active doctor associations for a clinic.
        
        Args:
            clinic_id: Clinic's ID
            
        Returns:
            List of active DoctorClinicAssociation instances
        """
        try:
            clinic_id_uuid = uuid.UUID(clinic_id)
            result = self.session.execute(
                select(DoctorClinicAssociation)
                .where(
                    and_(
                        DoctorClinicAssociation.clinic_id == clinic_id_uuid,
                        DoctorClinicAssociation.is_active == True
                    )
                )
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_association(self, doctor_id: str, clinic_id: str) -> Optional[DoctorClinicAssociation]:
        """
        Get a specific doctor-clinic association.
        
        Args:
            doctor_id: Doctor's ID
            clinic_id: Clinic's ID
            
        Returns:
            DoctorClinicAssociation instance or None
        """
        try:
            doctor_id_uuid = uuid.UUID(doctor_id)
            clinic_id_uuid = uuid.UUID(clinic_id)
            result = self.session.execute(
                select(DoctorClinicAssociation)
                .where(
                    and_(
                        DoctorClinicAssociation.doctor_id == doctor_id_uuid,
                        DoctorClinicAssociation.clinic_id == clinic_id_uuid
                    )
                )
            )
            return result.scalar_one_or_none()
        except (ValueError, AttributeError):
            return None
    
    def get_by_employment_type(
        self, 
        clinic_id: str, 
        employment_type: EmploymentType
    ) -> List[DoctorClinicAssociation]:
        """
        Get doctor associations for a clinic filtered by employment type.
        
        Args:
            clinic_id: Clinic's ID
            employment_type: Type of employment
            
        Returns:
            List of DoctorClinicAssociation instances
        """
        try:
            clinic_id_uuid = uuid.UUID(clinic_id)
            result = self.session.execute(
                select(DoctorClinicAssociation)
                .where(
                    and_(
                        DoctorClinicAssociation.clinic_id == clinic_id_uuid,
                        DoctorClinicAssociation.employment_type == employment_type,
                        DoctorClinicAssociation.is_active == True
                    )
                )
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []


