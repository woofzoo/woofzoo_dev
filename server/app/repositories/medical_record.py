"""
Medical Record repository for database operations.

This module provides the MedicalRecordRepository class for medical record-specific
database operations extending the base repository functionality.
"""

from typing import Optional, List
from datetime import datetime, date
import uuid

from sqlalchemy import select, and_, desc
from sqlalchemy.orm import Session

from app.models.medical_record import MedicalRecord, VisitType
from app.repositories.base import BaseRepository


class MedicalRecordRepository(BaseRepository[MedicalRecord]):
    """
    Medical Record repository for medical record-specific database operations.
    
    This class extends BaseRepository to provide medical record-specific
    database operations and queries.
    """
    
    def __init__(self, session: Session) -> None:
        """Initialize the medical record repository."""
        super().__init__(MedicalRecord, session)
    
    def get_by_pet_id(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """
        Get all medical records for a pet, ordered by visit date (newest first).
        
        Args:
            pet_id: Pet's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecord instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(MedicalRecord)
                .where(MedicalRecord.pet_id == pet_id_uuid)
                .order_by(desc(MedicalRecord.visit_date))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_pet_id_date_range(
        self, 
        pet_id: str, 
        start_date: datetime, 
        end_date: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[MedicalRecord]:
        """
        Get medical records for a pet within a date range.
        
        Args:
            pet_id: Pet's ID
            start_date: Start date for filtering
            end_date: End date for filtering
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecord instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(MedicalRecord)
                .where(
                    and_(
                        MedicalRecord.pet_id == pet_id_uuid,
                        MedicalRecord.visit_date >= start_date,
                        MedicalRecord.visit_date <= end_date
                    )
                )
                .order_by(desc(MedicalRecord.visit_date))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_clinic_id(self, clinic_id: str, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """
        Get all medical records for a specific clinic.
        
        Args:
            clinic_id: Clinic's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecord instances
        """
        try:
            clinic_id_uuid = uuid.UUID(clinic_id)
            result = self.session.execute(
                select(MedicalRecord)
                .where(MedicalRecord.clinic_id == clinic_id_uuid)
                .order_by(desc(MedicalRecord.visit_date))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_doctor_id(self, doctor_id: str, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """
        Get all medical records for a specific doctor.
        
        Args:
            doctor_id: Doctor's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecord instances
        """
        try:
            doctor_id_uuid = uuid.UUID(doctor_id)
            result = self.session.execute(
                select(MedicalRecord)
                .where(MedicalRecord.doctor_id == doctor_id_uuid)
                .order_by(desc(MedicalRecord.visit_date))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_by_visit_type(
        self, 
        pet_id: str, 
        visit_type: VisitType, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[MedicalRecord]:
        """
        Get medical records for a pet filtered by visit type.
        
        Args:
            pet_id: Pet's ID
            visit_type: Type of visit to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecord instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(MedicalRecord)
                .where(
                    and_(
                        MedicalRecord.pet_id == pet_id_uuid,
                        MedicalRecord.visit_type == visit_type
                    )
                )
                .order_by(desc(MedicalRecord.visit_date))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_emergency_records(self, pet_id: str, skip: int = 0, limit: int = 100) -> List[MedicalRecord]:
        """
        Get emergency medical records for a pet.
        
        Args:
            pet_id: Pet's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecord instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(MedicalRecord)
                .where(
                    and_(
                        MedicalRecord.pet_id == pet_id_uuid,
                        MedicalRecord.is_emergency == True
                    )
                )
                .order_by(desc(MedicalRecord.visit_date))
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []
    
    def get_records_requiring_followup(self, pet_id: str) -> List[MedicalRecord]:
        """
        Get medical records that require follow-up for a pet.
        
        Args:
            pet_id: Pet's ID
            
        Returns:
            List of MedicalRecord instances
        """
        try:
            pet_id_uuid = uuid.UUID(pet_id)
            result = self.session.execute(
                select(MedicalRecord)
                .where(
                    and_(
                        MedicalRecord.pet_id == pet_id_uuid,
                        MedicalRecord.follow_up_required == True,
                        MedicalRecord.follow_up_date >= date.today()
                    )
                )
                .order_by(MedicalRecord.follow_up_date)
            )
            return result.scalars().all()
        except (ValueError, AttributeError):
            return []


