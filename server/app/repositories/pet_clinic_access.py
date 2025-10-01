"""
Pet Clinic Access repository for database operations.

This module provides the PetClinicAccessRepository class for managing
clinic access to pet records.
"""

from typing import Optional, List
from datetime import datetime
import uuid

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

from app.models.pet_clinic_access import PetClinicAccess, AccessStatus
from app.repositories.base import BaseRepository


class PetClinicAccessRepository(BaseRepository[PetClinicAccess]):
    """
    Pet Clinic Access repository for managing clinic access to pet records.
    
    This class extends BaseRepository to provide pet clinic access-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the pet clinic access repository."""
        super().__init__(PetClinicAccess, session)
    
    def get_by_pet_id(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[PetClinicAccess]:
        """
        Get all access records for a pet.
        
        Args:
            pet_id: Pet's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of PetClinicAccess instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(PetClinicAccess)
                .where(PetClinicAccess.pet_id == pet_id_uuid)
                .order_by(desc(PetClinicAccess.access_granted_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_active_access(self, pet_id: str, clinic_id: str) -> Optional[PetClinicAccess]:
        """
        Get active access record for a pet at a specific clinic.
        
        Args:
            pet_id: Pet's ID
            clinic_id: Clinic's ID
            
        Returns:
            Active PetClinicAccess instance or None
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            clinic_id_uuid = uuid.UUID(clinic_id)
            now = datetime.utcnow()
            
            result = self.session.execute(
                select(PetClinicAccess)
                .where(
                    and_(
                        PetClinicAccess.pet_id == pet_id_uuid,
                        PetClinicAccess.clinic_id == clinic_id_uuid,
                        PetClinicAccess.status == AccessStatus.ACTIVE,
                        PetClinicAccess.access_expires_at > now
                    )
                )
            )
            return result.scalar_one_or_none()
        except (ValueError, AttributeError):
            return None
    
    def get_by_clinic_id(self, clinic_id: str, skip: int = 0, limit: int = 100) -> List[PetClinicAccess]:
        """
        Get all access records for a clinic.
        
        Args:
            clinic_id: Clinic's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of PetClinicAccess instances
        """
        try:
            clinic_id_uuid = uuid.UUID(clinic_id)
            result = self.session.execute(
                select(PetClinicAccess)
                .where(PetClinicAccess.clinic_id == clinic_id_uuid)
                .order_by(desc(PetClinicAccess.access_granted_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_active_by_clinic(self, clinic_id: str) -> List[PetClinicAccess]:
        """
        Get all active access records for a clinic.
        
        Args:
            clinic_id: Clinic's ID
            
        Returns:
            List of active PetClinicAccess instances
        """
        try:
            clinic_id_uuid = uuid.UUID(clinic_id)
            now = datetime.utcnow()
            
            result = self.session.execute(
                select(PetClinicAccess)
                .where(
                    and_(
                        PetClinicAccess.clinic_id == clinic_id_uuid,
                        PetClinicAccess.status == AccessStatus.ACTIVE,
                        PetClinicAccess.access_expires_at > now
                    )
                )
                .order_by(desc(PetClinicAccess.access_granted_at))
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_doctor_id(self, doctor_id: str, skip: int = 0, limit: int = 100) -> List[PetClinicAccess]:
        """
        Get all access records for a doctor.
        
        Args:
            doctor_id: Doctor's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of PetClinicAccess instances
        """
        try:
            doctor_id_uuid = uuid.UUID(doctor_id)
            result = self.session.execute(
                select(PetClinicAccess)
                .where(PetClinicAccess.doctor_id == doctor_id_uuid)
                .order_by(desc(PetClinicAccess.access_granted_at))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_expired_access(self, limit: int = 100) -> List[PetClinicAccess]:
        """
        Get expired access records that need status update.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of expired PetClinicAccess instances
        """
        now = datetime.utcnow()
        result = self.session.execute(
            select(PetClinicAccess)
            .where(
                and_(
                    PetClinicAccess.status == AccessStatus.ACTIVE,
                    PetClinicAccess.access_expires_at <= now
                )
            )
            .limit(limit)
        )
        return result.scalars().all()
    
    def revoke_access(self, access_id: str) -> bool:
        """
        Revoke a clinic's access to a pet.
        
        Args:
            access_id: Access record ID
            
        Returns:
            True if revoked, False otherwise
        """
        access = self.get_by_id(access_id)
        if access:
            access.status = AccessStatus.REVOKED
            self.session.commit()
            return True
        return False


