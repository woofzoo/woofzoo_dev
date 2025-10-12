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
    
    def get_medical_history_excluding(
        self,
        pet_id: uuid.UUID,
        exclude_record_id: uuid.UUID,
        limit: int = 10
    ) -> List[MedicalRecord]:
        """
        Get medical history for a pet, excluding a specific record.
        
        Args:
            pet_id: Pet UUID
            exclude_record_id: Medical record UUID to exclude
            limit: Maximum number of records to return
            
        Returns:
            List of MedicalRecord instances, ordered by visit date descending
        """
        medical_history = self.session.query(MedicalRecord).filter(
            and_(
                MedicalRecord.pet_id == pet_id,
                MedicalRecord.id != exclude_record_id
            )
        ).order_by(
            MedicalRecord.visit_date.desc()
        ).limit(limit).all()
        
        return medical_history
    
    def update_visit_record(
        self,
        medical_record_id: uuid.UUID,
        diagnosis: Optional[str] = None,
        treatment_plan: Optional[str] = None,
        clinical_notes: Optional[str] = None,
        vital_signs_update: Optional[dict] = None
    ) -> MedicalRecord:
        """
        Update a medical record with visit details.
        
        Args:
            medical_record_id: Medical record UUID
            diagnosis: Diagnosis text
            treatment_plan: Treatment plan
            clinical_notes: Clinical notes
            vital_signs_update: Vital signs to update/add
            
        Returns:
            Updated MedicalRecord instance
            
        Raises:
            ValueError: If record not found
        """
        medical_record = self.get(medical_record_id)
        if not medical_record:
            raise ValueError("Medical record not found")
        
        # Update fields
        if diagnosis is not None:
            medical_record.diagnosis = diagnosis
        if treatment_plan is not None:
            medical_record.treatment_plan = treatment_plan
        if clinical_notes is not None:
            medical_record.clinical_notes = clinical_notes
        
        # Update vital signs
        if vital_signs_update:
            existing_vitals = medical_record.vital_signs or {}
            existing_vitals.update(vital_signs_update)
            medical_record.vital_signs = existing_vitals
        
        return self.update_entity(medical_record)
    
    def update_follow_up(
        self,
        medical_record_id: uuid.UUID,
        follow_up_date: Optional[date] = None,
        follow_up_notes: Optional[str] = None
    ) -> MedicalRecord:
        """
        Update follow-up information for a medical record.
        
        Args:
            medical_record_id: Medical record UUID
            follow_up_date: Date for follow-up
            follow_up_notes: Follow-up instructions
            
        Returns:
            Updated MedicalRecord instance
            
        Raises:
            ValueError: If record not found
        """
        medical_record = self.get(medical_record_id)
        if not medical_record:
            raise ValueError("Medical record not found")
        
        if follow_up_date is not None:
            medical_record.follow_up_date = follow_up_date
            medical_record.follow_up_required = True
        if follow_up_notes is not None:
            medical_record.follow_up_notes = follow_up_notes
        
        return self.update_entity(medical_record)


