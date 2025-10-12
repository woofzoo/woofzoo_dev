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

from app.models.pet_clinic_access import PetClinicAccess, AccessStatus, QueueStatus
from app.models.medical_record import MedicalRecord
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

    def get_by_id(self, id: uuid.UUID) -> Optional[PetClinicAccess]:
        """
        Get a pet clinic access by id.
        """
        return self.session.get(PetClinicAccess, id)
    
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
    
    def count_active_in_queue(
        self, 
        queue_status: str, 
        assigned_before: datetime
    ) -> int:
        """
        Count pets in queue with given status assigned before datetime.
        
        Args:
            queue_status: Queue status to filter by
            assigned_before: Count only records assigned before this datetime
            
        Returns:
            Number of matching records
        """
        return self.session.query(PetClinicAccess).filter(
            PetClinicAccess.queue_status == queue_status,
            PetClinicAccess.assigned_to_doctor_at <= assigned_before
        ).count()
    
    def update_pre_check_vitals(
        self,
        access_record_id: uuid.UUID,
        weight: Optional[float],
        temperature: Optional[float],
        heart_rate: Optional[int],
        respiratory_rate: Optional[int],
        notes: Optional[str],
        completed_at: datetime,
        completed_by_user_id: uuid.UUID,
        new_queue_status: str
    ) -> PetClinicAccess:
        """
        Update pre-check vitals and queue status.
        
        Args:
            access_record_id: Access record UUID
            weight: Weight in kg
            temperature: Temperature in °C
            heart_rate: Heart rate in BPM
            respiratory_rate: Respiratory rate
            notes: Pre-check observations
            completed_at: Timestamp when pre-checks were completed
            completed_by_user_id: User who completed pre-checks
            new_queue_status: New queue status
            
        Returns:
            Updated PetClinicAccess instance
            
        Raises:
            ValueError: If access record not found
        """
        access = self.get_by_id(access_record_id)
        if not access:
            raise ValueError("Access record not found")
        
        access.pre_check_weight = weight
        access.pre_check_temperature = temperature
        access.pre_check_heart_rate = heart_rate
        access.pre_check_respiratory_rate = respiratory_rate
        access.pre_check_notes = notes
        access.pre_check_completed_at = completed_at
        access.pre_check_by_user_id = completed_by_user_id
        access.queue_status = new_queue_status
        
        return self.update_entity(access)
    
    def assign_to_doctor(
        self,
        access_record_id: uuid.UUID,
        medical_record_id: uuid.UUID,
        queue_status: str,
        assigned_at: datetime,
        queue_position: int
    ) -> PetClinicAccess:
        """
        Update access record for doctor assignment.
        
        Args:
            access_record_id: Access record UUID
            medical_record_id: Medical record UUID
            queue_status: New queue status
            assigned_at: Timestamp when assigned
            queue_position: Position in queue
            
        Returns:
            Updated PetClinicAccess instance
            
        Raises:
            ValueError: If access record not found
        """
        access = self.get(access_record_id)
        if not access:
            raise ValueError("Access record not found")
        
        access.medical_record_id = medical_record_id
        access.queue_status = queue_status
        access.assigned_to_doctor_at = assigned_at
        access.queue_position = queue_position
        
        return self.update_entity(access)
    
    def get_todays_queue_for_doctor(
        self,
        doctor_id: uuid.UUID,
        start_date: datetime,
        end_date: datetime
    ) -> List[PetClinicAccess]:
        """
        Get all access records assigned to a doctor for a specific date range.
        
        Args:
            doctor_id: Doctor UUID
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            List of PetClinicAccess instances for the doctor's queue
        """
        queue_items = self.session.query(PetClinicAccess).filter(
            and_(
                PetClinicAccess.medical_record_id.isnot(None),
                PetClinicAccess.assigned_to_doctor_at >= start_date,
                PetClinicAccess.assigned_to_doctor_at < end_date,
                PetClinicAccess.queue_status.in_([QueueStatus.WITH_DOCTOR, QueueStatus.COMPLETED])
            )
        ).join(
            MedicalRecord,
            PetClinicAccess.medical_record_id == MedicalRecord.id
        ).filter(
            MedicalRecord.doctor_id == doctor_id
        ).order_by(
            PetClinicAccess.queue_position
        ).all()
        
        return queue_items
    
    def get_by_medical_record_id(self, medical_record_id: uuid.UUID) -> Optional[PetClinicAccess]:
        """
        Get access record by medical record ID.
        
        Args:
            medical_record_id: Medical record UUID
            
        Returns:
            PetClinicAccess instance or None
        """
        return self.session.query(PetClinicAccess).filter(
            PetClinicAccess.medical_record_id == medical_record_id
        ).first()
    
    def complete_visit(
        self,
        medical_record_id: uuid.UUID,
        completed_at: datetime
    ) -> Optional[PetClinicAccess]:
        """
        Mark a visit as completed.
        
        Args:
            medical_record_id: Medical record UUID
            completed_at: Completion timestamp
            
        Returns:
            Updated PetClinicAccess instance or None if not found
        """
        access = self.get_by_medical_record_id(medical_record_id)
        if access:
            access.queue_status = QueueStatus.COMPLETED.value
            access.visit_completed_at = completed_at
            return self.update_entity(access)
        return None


